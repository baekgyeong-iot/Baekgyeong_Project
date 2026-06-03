from __future__ import annotations

import threading
import time
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

from game_logic import state
from game_logic.event_handler import handle_event
from game_logic.logic import get_led_state


TICK_INTERVAL_SECONDS = 60

app = Flask(__name__)
CORS(app)


RANKINGS: dict[str, list[dict[str, Any]]] = {
    "blue_red_flag": [],
    "memory": [],
    "red_light_green_light": [],
}

INVENTORY: list[dict[str, Any]] = []


def apply_startup_progress() -> None:
    handle_event(
        {
            "source": "SYSTEM",
            "event": "APPLY_OFFLINE_PROGRESS",
            "payload": {
                "tick_interval_seconds": TICK_INTERVAL_SECONDS,
            },
        }
    )


def time_tick_loop() -> None:
    while True:
        time.sleep(TICK_INTERVAL_SECONDS)
        handle_event(
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


def start_background_tasks() -> None:
    apply_startup_progress()
    threading.Thread(target=time_tick_loop, daemon=True).start()


@app.get("/api/state")
def get_current_state():
    return jsonify(state.get_state())


@app.get("/api/logs")
def get_logs():
    limit = request.args.get("limit", default=30, type=int)
    return jsonify({"logs": state.get_logs(limit)})


@app.get("/api/rankings")
def get_rankings():
    return jsonify(
        {
            "rankings": RANKINGS,
            "notice": "랭킹은 대시보드에서 확인할 수 있습니다.",
        }
    )


@app.get("/api/inventory")
def get_inventory():
    return jsonify(
        {
            "gifts": INVENTORY,
            "notice": "받은 선물은 대시보드에서 확인할 수 있습니다.",
        }
    )


@app.get("/api/led")
def get_led():
    return jsonify(get_led_state())


@app.post("/api/event")
def post_event():
    event_message = request.get_json(silent=True) or {}
    result = handle_event(event_message)
    return jsonify(
        {
            "result": result,
            "state": state.get_state(),
            "led": get_led_state(),
        }
    )


@app.post("/api/reset")
def reset_baekgyeong():
    payload = request.get_json(silent=True) or {}
    new_state = state.reset_state(payload.get("birth_date"))
    return jsonify(new_state)


if __name__ == "__main__":
    start_background_tasks()
    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)
