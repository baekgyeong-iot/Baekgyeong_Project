from __future__ import annotations

from typing import Any

try:
    from . import evolution, logic, state
except ImportError:
    import evolution  # type: ignore
    import logic  # type: ignore
    import state  # type: ignore


# 이 파일은 game_logic의 입구 역할을 한다.
# UI, LCD, MQTT, Flask API는 모두 {source, event, payload} 형태의 메시지를 만들고
# handle_event()는 event 이름에 맞는 실제 로직 함수로 연결한다.
def _payload(event_message: dict[str, Any]) -> dict[str, Any]:
    payload = event_message.get("payload")
    if isinstance(payload, dict):
        return payload
    return {}


def handle_event(event_message: dict[str, Any]) -> dict[str, Any]:
    """외부 이벤트를 받아 백경이 상태 변경 함수로 라우팅한다."""
    event_name = event_message.get("event")
    payload = _payload(event_message)

    # 먹기 게임은 UI/LCD가 최종 결과만 전달한다.
    # game_logic은 hunger 증가와 feed_count 증가를 담당한다.
    if event_name == "FEED_GAME_FINISHED":
        result = logic.feed(
            hunger_delta=int(payload.get("hunger_delta", 0)),
            caught_food_ids=list(payload.get("caught_food_ids", [])),
        )
        evolution.check_evolution(trigger="action_performed")
        return result

    # 놀이 게임도 화면별 점수 계산은 UI가 하고,
    # game_logic은 fun 증가, play_count 증가, 랭킹 저장을 담당한다.
    if event_name == "PLAY_GAME_FINISHED":
        result = logic.play(
            game_type=str(payload.get("game_type", "unknown")),
            score=int(payload.get("score", 0)),
            fun_delta=int(payload.get("fun_delta", 0)),
            date_string=payload.get("date"),
        )
        evolution.check_evolution(trigger="action_performed")
        return result

    # 그냥 놀기는 LCD 화면에서 제한 시간 동안 센서 입력을 누적한다.
    # 여기서는 센서 이벤트를 로그로 남기고, 최종 결과는 LCD가 PLAY_GAME_FINISHED로 보낸다.
    if event_name == "GYRO_CHANGED":
        direction = str(payload.get("tilt_direction", "")).upper()
        if direction in {"LEFT", "RIGHT", "FORWARD", "BACKWARD"}:
            return state.add_log(
                "GYRO_CHANGED",
                {**payload, "tilt_direction": direction},
                source=event_message.get("source", "GYRO"),
            )
        return state.add_log("GYRO_CHANGED_IGNORED", payload, source=event_message.get("source", "GYRO"))

    if event_name == "DEVICE_SHAKEN":
        return state.add_log(
            "DEVICE_SHAKEN",
            {
                **payload,
                "shake_power": int(payload.get("shake_power", 1)),
            },
            source=event_message.get("source", "GYRO"),
        )

    if event_name == "GIFT_EVENT_TRIGGERED":
        return logic.receive_gift(gift_id=int(payload.get("gift_id", 1)))

    # 잠은 시작/회복 tick/종료를 분리해서 처리한다.
    if event_name == "SLEEP_STARTED":
        return logic.start_sleep()

    if event_name == "SLEEP_TICK":
        return logic.sleep_tick(energy_delta=int(payload.get("energy_delta", 1)))

    if event_name == "SLEEP_ENDED":
        result = logic.end_sleep(full_energy_delta=int(payload.get("full_energy_delta", 0)))
        evolution.check_evolution(trigger="action_performed")
        return result

    # 서버나 메인 루프가 주기적으로 호출하는 시간 흐름 이벤트다.
    if event_name == "TIME_TICK":
        return logic.time_tick(
            hunger_delta=int(payload.get("hunger_delta", -1)),
            fun_delta=int(payload.get("fun_delta", -1)),
            energy_delta=int(payload.get("energy_delta", -1)),
        )

    # 서버가 꺼져 있던 동안의 시간 경과를 한 번에 반영한다.
    if event_name == "APPLY_OFFLINE_PROGRESS":
        return logic.apply_offline_progress(
            tick_interval_seconds=int(payload.get("tick_interval_seconds", 60)),
            hunger_delta=int(payload.get("hunger_delta", -1)),
            fun_delta=int(payload.get("fun_delta", -1)),
            energy_delta=int(payload.get("energy_delta", -1)),
        )

    # 조도 센서는 어두워지면 잠 시작, 자는 중 밝아지면 잠 종료로 해석한다.
    if event_name == "LIGHT_CHANGED":
        is_dark = bool(payload.get("is_dark", False))
        if is_dark and not state.baekgyeong_state["is_sleeping"]:
            return logic.start_sleep()
        if not is_dark and state.baekgyeong_state["is_sleeping"]:
            return logic.end_sleep(full_energy_delta=int(payload.get("full_energy_delta", 0)))
        return state.add_log("LIGHT_CHANGED", payload, source=event_message.get("source", "LIGHT_SENSOR"))

    # 쓰다듬기는 하루 1회 성공 가능하다.
    if event_name == "STROKE_ATTEMPT":
        return logic.stroke(date_string=payload.get("date"))

    # 청기백기 게임에서 외부 LED를 왼쪽/오른쪽/꺼짐으로 제어하기 위한 이벤트다.
    if event_name == "LED_LEFT":
        return logic.set_game_led("LEFT")

    if event_name == "LED_RIGHT":
        return logic.set_game_led("RIGHT")

    if event_name == "LED_OFF":
        return logic.set_game_led("OFF")

    if event_name == "EVO_CHECK":
        return evolution.check_evolution(
            trigger=str(payload.get("trigger", "manual")),
            date_string=payload.get("date"),
        )

    # 개발/테스트용 수동 검사 이벤트들.
    if event_name == "RUNAWAY_CHECK":
        return logic.check_runaway(date_string=payload.get("date"))

    if event_name == "NEW_BAEKGYEONG_REQUESTED":
        return logic.new_baekgyeong(date_string=payload.get("birth_date"))

    return state.add_log(
        "UNHANDLED_EVENT",
        {"event": event_name, "payload": payload},
        source=event_message.get("source", "SYSTEM"),
    )


def handle_sensor_event(source: str, event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """센서 코드에서 source/event/payload를 따로 넘기고 싶을 때 쓰는 편의 함수."""
    return handle_event({"source": source, "event": event, "payload": payload or {}})
