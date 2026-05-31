from __future__ import annotations

from typing import Any

try:
    from . import evolution, logic, state
except ImportError:
    import evolution  # type: ignore
    import logic  # type: ignore
    import state  # type: ignore


def _payload(event_message: dict[str, Any]) -> dict[str, Any]:
    payload = event_message.get("payload")
    if isinstance(payload, dict):
        return payload
    return {}


def handle_event(event_message: dict[str, Any]) -> dict[str, Any]:
    event_name = event_message.get("event")
    payload = _payload(event_message)

    if event_name == "FEED_GAME_FINISHED":
        result = logic.feed(
            hunger_delta=int(payload.get("hunger_delta", 0)),
            caught_food_ids=list(payload.get("caught_food_ids", [])),
        )
        evolution.check_evolution(trigger="action_performed")
        return result

    if event_name == "PLAY_GAME_FINISHED":
        result = logic.play(
            game_type=str(payload.get("game_type", "unknown")),
            score=int(payload.get("score", 0)),
            fun_delta=int(payload.get("fun_delta", 0)),
        )
        evolution.check_evolution(trigger="action_performed")
        return result

    if event_name == "SLEEP_STARTED":
        return logic.start_sleep()

    if event_name == "SLEEP_TICK":
        return logic.sleep_tick(energy_delta=int(payload.get("energy_delta", 1)))

    if event_name == "SLEEP_ENDED":
        result = logic.end_sleep(full_energy_delta=int(payload.get("full_energy_delta", 0)))
        evolution.check_evolution(trigger="action_performed")
        return result

    if event_name == "TIME_TICK":
        return logic.time_tick(
            hunger_delta=int(payload.get("hunger_delta", -1)),
            fun_delta=int(payload.get("fun_delta", -1)),
            energy_delta=int(payload.get("energy_delta", -1)),
        )

    if event_name == "APPLY_OFFLINE_PROGRESS":
        return logic.apply_offline_progress(
            tick_interval_seconds=int(payload.get("tick_interval_seconds", 60)),
            hunger_delta=int(payload.get("hunger_delta", -1)),
            fun_delta=int(payload.get("fun_delta", -1)),
            energy_delta=int(payload.get("energy_delta", -1)),
        )

    if event_name == "LIGHT_CHANGED":
        is_dark = bool(payload.get("is_dark", False))
        if is_dark and not state.baekgyeong_state["is_sleeping"]:
            return logic.start_sleep()
        if not is_dark and state.baekgyeong_state["is_sleeping"]:
            return logic.end_sleep(full_energy_delta=int(payload.get("full_energy_delta", 0)))
        return state.add_log("LIGHT_CHANGED", payload, source=event_message.get("source", "LIGHT_SENSOR"))

    if event_name == "STROKE_ATTEMPT":
        return logic.stroke(date_string=payload.get("date"))

    if event_name == "EVO_CHECK":
        return evolution.check_evolution(
            trigger=str(payload.get("trigger", "manual")),
            date_string=payload.get("date"),
        )

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
    return handle_event({"source": source, "event": event, "payload": payload or {}})
