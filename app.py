from __future__ import annotations

import threading
import time
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

from game_logic import state
from game_logic.event_handler import handle_event
from game_logic.logic import get_led_state

try:
    from mqtt_client import BaekgyeongMqttClient
except Exception as exc:  # MQTT 의존성이 없어도 Flask 서버는 실행되어야 한다.
    BaekgyeongMqttClient = None  # type: ignore[assignment]
    MQTT_IMPORT_ERROR = exc
else:
    MQTT_IMPORT_ERROR = None


# Flask 서버가 담당하는 시간 흐름 단위.
# 일반 수치 감소와 수면 회복은 체감 속도가 달라서 따로 움직인다.
DECAY_TICK_INTERVAL_SECONDS = 10
SLEEP_TICK_INTERVAL_SECONDS = 2

app = Flask(__name__)
CORS(app)


MQTT_BRIDGE = None


def apply_startup_progress() -> None:
    """서버가 꺼져 있던 동안의 시간 경과를 게임 상태에 반영한다."""
    handle_event(
        {
            "source": "SYSTEM",
            "event": "APPLY_OFFLINE_PROGRESS",
            "payload": {
                "tick_interval_seconds": DECAY_TICK_INTERVAL_SECONDS,
            },
        }
    )


def time_tick_loop() -> None:
    """서버 실행 중 주기적으로 배고픔/재미/기력 감소 이벤트를 발생시킨다."""
    while True:
        time.sleep(DECAY_TICK_INTERVAL_SECONDS)
        result = handle_event(
            {
                "source": "SYSTEM",
                "event": "TIME_TICK",
                "payload": {
                    "hunger_delta": -1,
                    "fun_delta": -1,
                    "energy_delta": -1,
                },
            }
        )
        if MQTT_BRIDGE is not None:
            MQTT_BRIDGE.publish_state_update(result)


def sleep_tick_loop() -> None:
    """백경이가 자는 동안 더 짧은 주기로 기력을 회복시킨다."""
    while True:
        time.sleep(SLEEP_TICK_INTERVAL_SECONDS)
        if state.baekgyeong_state.get("is_sleeping"):
            sleep_result = handle_event(
                {
                    "source": "SYSTEM",
                    "event": "SLEEP_TICK",
                    "payload": {
                        "energy_delta": 1,
                    },
                }
            )
            if MQTT_BRIDGE is not None:
                MQTT_BRIDGE.publish_state_update(sleep_result)


def start_background_tasks() -> None:
    """서버 시작 시 필요한 자동 작업들을 등록한다."""
    state.baekgyeong_state["game_led"] = "OFF"
    state.save_game()
    apply_startup_progress()
    threading.Thread(target=time_tick_loop, daemon=True).start()
    threading.Thread(target=sleep_tick_loop, daemon=True).start()
    start_mqtt_bridge()


def start_mqtt_bridge() -> None:
    """MQTT 메시지도 Flask와 같은 game_logic 상태에서 처리되도록 브릿지를 켠다."""
    global MQTT_BRIDGE

    if BaekgyeongMqttClient is None:
        print("[MQTT DISABLED]", MQTT_IMPORT_ERROR)
        return

    try:
        MQTT_BRIDGE = BaekgyeongMqttClient(client_id="baekgyeong-flask-server")
        MQTT_BRIDGE.loop_start()
        MQTT_BRIDGE.publish_state_update()
        print("[MQTT BRIDGE STARTED]")
    except Exception as exc:
        MQTT_BRIDGE = None
        print("[MQTT BRIDGE DISABLED]", type(exc).__name__, exc)


@app.get("/api/state")
def get_current_state():
    """웹 대시보드와 LCD가 현재 백경이 상태를 조회할 때 사용한다."""
    return jsonify(state.get_state())


@app.get("/api/logs")
def get_logs():
    """최근 이벤트 로그를 조회한다."""
    limit = request.args.get("limit", default=30, type=int)
    return jsonify({"logs": state.get_logs(limit)})


@app.get("/api/rankings")
def get_rankings():
    """게임별 랭킹을 score 내림차순으로 조회한다."""
    return jsonify(
        {
            "rankings": state.get_rankings(),
            "notice": "랭킹은 대시보드에서 확인할 수 있습니다.",
        }
    )


@app.get("/api/inventory")
def get_inventory():
    """백경이가 가져온 선물 인벤토리를 조회한다."""
    return jsonify(
        {
            "gifts": state.get_inventory(),
            "notice": "받은 선물은 대시보드에서 확인할 수 있습니다.",
        }
    )


@app.get("/api/led")
def get_led():
    """현재 상태를 기준으로 LED가 어떤 색이어야 하는지 반환한다."""
    return jsonify(get_led_state())


@app.post("/api/event")
def post_event():
    """LCD, 웹, IoT 쪽에서 발생한 이벤트를 game_logic으로 전달한다."""
    event_message = request.get_json(silent=True) or {}
    result = handle_event(event_message)
    if MQTT_BRIDGE is not None:
        MQTT_BRIDGE.publish_state_update(result)
    return jsonify(
        {
            "result": result,
            "state": state.get_state(),
            "led": get_led_state(),
        }
    )


@app.post("/api/reset")
def reset_baekgyeong():
    """백경이를 새로 키우는 상태로 초기화한다."""
    payload = request.get_json(silent=True) or {}
    new_state = state.reset_state(payload.get("birth_date"))
    return jsonify(new_state)


if __name__ == "__main__":
    start_background_tasks()
    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)
