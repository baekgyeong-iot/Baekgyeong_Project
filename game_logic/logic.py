from __future__ import annotations

from datetime import date, datetime
from typing import Any

try:
    from . import state
except ImportError:
    import state  # type: ignore


LOW_STAT_THRESHOLD = 50
RUNAWAY_LOW_THRESHOLD = 10


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def days_between(start: str, end: str | None = None) -> int:
    end_date = _parse_date(end) or date.today()
    start_date = _parse_date(start)
    if start_date is None:
        return 0
    return max(0, (end_date - start_date).days)


def calculate_mood() -> str:
    current = state.baekgyeong_state
    if current["is_runaway"]:
        return state.MOOD_RUNAWAY
    if current["is_sleeping"]:
        return state.MOOD_SLEEPING
    if current["hunger"] <= LOW_STAT_THRESHOLD:
        return state.MOOD_HUNGRY
    if current["energy"] <= LOW_STAT_THRESHOLD:
        return state.MOOD_SLEEPY
    if current["fun"] <= LOW_STAT_THRESHOLD:
        return state.MOOD_BORED
    if current["hunger"] >= 80 and current["fun"] >= 80 and current["energy"] >= 80:
        return state.MOOD_HAPPY
    return state.MOOD_NORMAL


def refresh_mood() -> str:
    mood = calculate_mood()
    state.baekgyeong_state["mood"] = mood
    return mood


def led_color(value: int) -> str:
    if value <= 30:
        return "RED"
    if value <= 50:
        return "YELLOW"
    return "GREEN"


def get_led_state() -> dict[str, str]:
    current = state.baekgyeong_state
    return {
        "hunger_led": led_color(current["hunger"]),
        "energy_led": led_color(current["energy"]),
        "fun_led": led_color(current["fun"]),
    }


def decay_stats(hunger_delta: int = -1, fun_delta: int = -1, energy_delta: int = -1) -> dict[str, Any]:
    if state.baekgyeong_state["is_runaway"]:
        return state.get_state()
    state.adjust_stat("hunger", hunger_delta)
    state.adjust_stat("fun", fun_delta)
    if not state.baekgyeong_state["is_sleeping"]:
        state.adjust_stat("energy", energy_delta)
    refresh_mood()
    check_runaway()
    return state.get_state()


def time_tick(hunger_delta: int = -1, fun_delta: int = -1, energy_delta: int = -1) -> dict[str, Any]:
    before = state.get_state()
    after = decay_stats(hunger_delta, fun_delta, energy_delta)
    state.baekgyeong_state["last_tick_at"] = state.now_string()
    return state.add_log(
        "TIME_TICK",
        {
            "hunger_delta": after["hunger"] - before["hunger"],
            "fun_delta": after["fun"] - before["fun"],
            "energy_delta": after["energy"] - before["energy"],
            "hunger": after["hunger"],
            "fun": after["fun"],
            "energy": after["energy"],
        },
    )


def _ceil_div(value: int, divisor: int) -> int:
    return (value + divisor - 1) // divisor


def _ticks_until_zero(value: int, delta: int) -> int | None:
    if delta >= 0:
        return None
    if value <= 0:
        return 0
    return _ceil_div(value, abs(delta))


def _ticks_until_under_ten(value: int, delta: int) -> int | None:
    if delta >= 0:
        return None
    if value <= RUNAWAY_LOW_THRESHOLD:
        return 0
    return _ceil_div(value - RUNAWAY_LOW_THRESHOLD, abs(delta))


def _offline_runaway_tick(before: dict[str, Any], hunger_delta: int, fun_delta: int, energy_delta: int) -> int | None:
    zero_ticks = [
        tick
        for tick in [
            _ticks_until_zero(before["hunger"], hunger_delta),
            _ticks_until_zero(before["fun"], fun_delta),
            _ticks_until_zero(before["energy"], energy_delta),
        ]
        if tick is not None
    ]

    under_ten_ticks = [
        _ticks_until_under_ten(before["hunger"], hunger_delta),
        _ticks_until_under_ten(before["fun"], fun_delta),
        _ticks_until_under_ten(before["energy"], energy_delta),
    ]
    all_under_ten_tick = None
    if all(tick is not None for tick in under_ten_ticks):
        all_under_ten_tick = max(tick for tick in under_ten_ticks if tick is not None)

    candidates = zero_ticks
    if all_under_ten_tick is not None:
        candidates.append(all_under_ten_tick)
    if not candidates:
        return None
    return min(candidates)


def apply_offline_progress(
    tick_interval_seconds: int = 60,
    hunger_delta: int = -1,
    fun_delta: int = -1,
    energy_delta: int = -1,
) -> dict[str, Any]:
    if state.baekgyeong_state["is_runaway"]:
        return state.add_log("OFFLINE_PROGRESS_SKIPPED", {"reason": "is_runaway"})

    now = datetime.now()
    last_tick = _parse_datetime(state.baekgyeong_state.get("last_tick_at"))
    if last_tick is None:
        state.baekgyeong_state["last_tick_at"] = state.now_string()
        return state.add_log("OFFLINE_PROGRESS_SKIPPED", {"reason": "missing_last_tick_at"})

    elapsed_seconds = int((now - last_tick).total_seconds())
    ticks = elapsed_seconds // tick_interval_seconds
    if ticks <= 0:
        return state.add_log(
            "OFFLINE_PROGRESS_SKIPPED",
            {"reason": "not_enough_elapsed_time", "elapsed_seconds": elapsed_seconds},
        )

    before = state.get_state()
    state.adjust_stat("hunger", hunger_delta * ticks)
    state.adjust_stat("fun", fun_delta * ticks)
    if not state.baekgyeong_state["is_sleeping"]:
        state.adjust_stat("energy", energy_delta * ticks)
    state.baekgyeong_state["last_tick_at"] = state.now_string()
    refresh_mood()

    ticks_per_day = max(1, 86400 // tick_interval_seconds)
    danger_tick = _offline_runaway_tick(before, hunger_delta, fun_delta, energy_delta)
    reason = _runaway_reason()
    if danger_tick is not None and reason is not None and ticks - danger_tick >= ticks_per_day:
        runaway_event = trigger_runaway(reason, state.today_string())
    else:
        runaway_event = check_runaway()

    after = state.get_state()
    return state.add_log(
        "OFFLINE_PROGRESS_APPLIED",
        {
            "elapsed_seconds": elapsed_seconds,
            "ticks": ticks,
            "hunger_delta": after["hunger"] - before["hunger"],
            "fun_delta": after["fun"] - before["fun"],
            "energy_delta": after["energy"] - before["energy"],
            "hunger": after["hunger"],
            "fun": after["fun"],
            "energy": after["energy"],
            "runaway_event": runaway_event["event"],
        },
    )


def feed(hunger_delta: int, caught_food_ids: list[int] | None = None) -> dict[str, Any]:
    if state.baekgyeong_state["is_runaway"]:
        return state.add_log("ACTION_IGNORED", {"reason": "is_runaway", "action": "feed"})
    new_hunger = state.adjust_stat("hunger", hunger_delta)
    if hunger_delta > 0:
        state.increment_count("feed_count")
    refresh_mood()
    check_runaway()
    payload = {
        "caught_food_ids": caught_food_ids or [],
        "hunger_delta": hunger_delta,
        "current_hunger": new_hunger,
    }
    return state.add_log("FEED_GAME_FINISHED", payload, source="LCD")


def play(game_type: str, score: int, fun_delta: int) -> dict[str, Any]:
    if state.baekgyeong_state["is_runaway"]:
        return state.add_log("ACTION_IGNORED", {"reason": "is_runaway", "action": "play"})
    new_fun = state.adjust_stat("fun", fun_delta)
    if fun_delta > 0:
        state.increment_count("play_count")
    refresh_mood()
    check_runaway()
    payload = {
        "game_type": game_type,
        "score": score,
        "fun_delta": fun_delta,
        "current_fun": new_fun,
    }
    return state.add_log("PLAY_GAME_FINISHED", payload, source="LCD")


def start_sleep() -> dict[str, Any]:
    if state.baekgyeong_state["is_runaway"]:
        return state.add_log("ACTION_IGNORED", {"reason": "is_runaway", "action": "sleep"})
    state.baekgyeong_state["is_sleeping"] = True
    refresh_mood()
    return state.add_log("SLEEP_STARTED")


def sleep_tick(energy_delta: int = 1) -> dict[str, Any]:
    if not state.baekgyeong_state["is_sleeping"]:
        return state.add_log("SLEEP_TICK_IGNORED", {"reason": "not_sleeping"})
    current_energy = state.adjust_stat("energy", energy_delta)
    refresh_mood()
    return state.add_log("SLEEP_TICK", {"energy_delta": energy_delta, "current_energy": current_energy})


def end_sleep(full_energy_delta: int) -> dict[str, Any]:
    state.baekgyeong_state["is_sleeping"] = False
    if full_energy_delta > 0:
        state.adjust_stat("energy", full_energy_delta)
        state.increment_count("sleep_count")
    refresh_mood()
    check_runaway()
    return state.add_log(
        "SLEEP_ENDED",
        {
            "full_energy_delta": full_energy_delta,
            "current_energy": state.baekgyeong_state["energy"],
        },
    )


def stroke(date_string: str | None = None, favorability_delta: int = 5) -> dict[str, Any]:
    current_date = date_string or state.today_string()
    if state.baekgyeong_state["last_stroke_time"] == current_date:
        return state.add_log(
            "STROKE_RESULT",
            {
                "success": False,
                "favorability_delta": 0,
                "current_favorability": state.baekgyeong_state["favorability"],
                "date": current_date,
            },
        )
    current_favorability = state.adjust_stat("favorability", favorability_delta)
    state.baekgyeong_state["last_stroke_time"] = current_date
    refresh_mood()
    return state.add_log(
        "STROKE_RESULT",
        {
            "success": True,
            "favorability_delta": favorability_delta,
            "current_favorability": current_favorability,
            "date": current_date,
        },
    )


def _runaway_reason() -> str | None:
    current = state.baekgyeong_state
    if current["hunger"] == 0:
        return "hunger_zero"
    if current["fun"] == 0:
        return "fun_zero"
    if current["energy"] == 0:
        return "energy_zero"
    if (
        current["hunger"] <= RUNAWAY_LOW_THRESHOLD
        and current["fun"] <= RUNAWAY_LOW_THRESHOLD
        and current["energy"] <= RUNAWAY_LOW_THRESHOLD
    ):
        return "all_stat_under_ten"
    return None


def check_runaway(date_string: str | None = None) -> dict[str, Any]:
    current_date = date_string or state.today_string()
    reason = _runaway_reason()

    if reason is None:
        state.baekgyeong_state["runaway_ready_date"] = None
        return state.add_log(
            "RUNAWAY_CHECK",
            {
                "hunger": state.baekgyeong_state["hunger"],
                "fun": state.baekgyeong_state["fun"],
                "energy": state.baekgyeong_state["energy"],
                "date": current_date,
                "runaway_ready_date": None,
            },
        )

    ready_date = state.baekgyeong_state["runaway_ready_date"]
    if ready_date is None:
        state.baekgyeong_state["runaway_ready_date"] = current_date
    elif days_between(ready_date, current_date) >= 1:
        return trigger_runaway(reason, current_date)

    return state.add_log(
        "RUNAWAY_CHECK",
        {
            "hunger": state.baekgyeong_state["hunger"],
            "fun": state.baekgyeong_state["fun"],
            "energy": state.baekgyeong_state["energy"],
            "date": current_date,
            "runaway_ready_date": state.baekgyeong_state["runaway_ready_date"],
        },
    )


def trigger_runaway(reason: str, date_string: str | None = None) -> dict[str, Any]:
    current_date = date_string or state.today_string()
    state.baekgyeong_state["is_runaway"] = True
    refresh_mood()
    return state.add_log(
        "RUNAWAY_EVENT_TRIGGERED",
        {
            "reason": reason,
            "hunger": state.baekgyeong_state["hunger"],
            "fun": state.baekgyeong_state["fun"],
            "energy": state.baekgyeong_state["energy"],
            "date": current_date,
        },
    )


def new_baekgyeong(date_string: str | None = None) -> dict[str, Any]:
    new_state = state.reset_state(date_string)
    return state.add_log(
        "NEW_BAEKGYEONG_REQUESTED",
        {
            "birth_date": new_state["birth_date"],
            "growth_stage": new_state["growth_stage"],
        },
        source="LCD",
    )
