from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime
import json
from pathlib import Path
from typing import Any


MIN_STAT = 0
MAX_STAT = 100

DEFAULT_HUNGER = 40
DEFAULT_FUN = 40
DEFAULT_ENERGY = 40
DEFAULT_FAVORABILITY = 0

MOOD_NORMAL = "NORMAL"
MOOD_HAPPY = "HAPPY"
MOOD_HUNGRY = "HUNGRY"
MOOD_SLEEPY = "SLEEPY"
MOOD_BORED = "BORED"
MOOD_SLEEPING = "SLEEPING"
MOOD_RUNAWAY = "RUNAWAY"

STAGE_BABY = "BABY"
STAGE_CHILD = "CHILD"
STAGE_ADULT = "ADULT"

SAVE_PATH = Path(__file__).with_name("baekgyeong_save.json")


# state.py는 현재 백경이 상태와 저장 파일을 관리한다.
# 다른 파일은 가능하면 get_state(), adjust_stat(), add_log() 같은 함수를 통해 상태를 바꾼다.
def today_string() -> str:
    return date.today().isoformat()


def now_string() -> str:
    return datetime.now().isoformat(timespec="seconds")


def clamp_stat(value: int) -> int:
    return max(MIN_STAT, min(MAX_STAT, int(value)))


def _initial_state(birth_date: str | None = None) -> dict[str, Any]:
    return {
        "birth_date": birth_date or today_string(),
        "hunger": DEFAULT_HUNGER,
        "fun": DEFAULT_FUN,
        "energy": DEFAULT_ENERGY,
        "favorability": DEFAULT_FAVORABILITY,
        "mood": MOOD_NORMAL,
        "growth_stage": STAGE_BABY,
        "is_sleeping": False,
        "last_stroke_time": None,
        "last_gift_received_date": None,
        "last_gift_check_date": None,
        "feed_count": 0,
        "play_count": 0,
        "sleep_count": 0,
        "runaway_ready_date": None,
        "is_runaway": False,
        "game_led": "OFF",
        "last_tick_at": now_string(),
        "last_saved_at": now_string(),
    }


baekgyeong_state: dict[str, Any] = _initial_state()
event_logs: list[dict[str, Any]] = []


def get_state() -> dict[str, Any]:
    return deepcopy(baekgyeong_state)


def reset_state(birth_date: str | None = None) -> dict[str, Any]:
    baekgyeong_state.clear()
    baekgyeong_state.update(_initial_state(birth_date))
    add_log("NEW_BAEKGYEONG_STARTED", {"birth_date": baekgyeong_state["birth_date"]})
    return get_state()


def set_value(key: str, value: Any) -> dict[str, Any]:
    baekgyeong_state[key] = value
    save_game()
    return get_state()


def set_stat(key: str, value: int) -> int:
    if key not in {"hunger", "fun", "energy", "favorability"}:
        raise KeyError(f"{key} is not a managed stat")
    baekgyeong_state[key] = clamp_stat(value)
    save_game()
    return baekgyeong_state[key]


def adjust_stat(key: str, delta: int) -> int:
    return set_stat(key, int(baekgyeong_state[key]) + int(delta))


def increment_count(key: str) -> int:
    if key not in {"feed_count", "play_count", "sleep_count"}:
        raise KeyError(f"{key} is not an action counter")
    baekgyeong_state[key] = int(baekgyeong_state[key]) + 1
    save_game()
    return baekgyeong_state[key]


def make_event(source: str, event: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "source": source,
        "event": event,
        "timestamp": now_string(),
        "payload": payload or {},
    }


def add_log(event: str, payload: dict[str, Any] | None = None, source: str = "SYSTEM") -> dict[str, Any]:
    log = make_event(source, event, payload)
    event_logs.append(log)
    save_game()
    return log


def get_logs(limit: int | None = None) -> list[dict[str, Any]]:
    logs = deepcopy(event_logs)
    if limit is None:
        return logs
    return logs[-limit:]


def state_updated_event() -> dict[str, Any]:
    return add_log("STATE_UPDATED", get_state())


def save_game() -> None:
    baekgyeong_state["last_saved_at"] = now_string()
    data = {
        "state": baekgyeong_state,
        "event_logs": event_logs[-100:],
    }
    SAVE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_game() -> dict[str, Any]:
    if not SAVE_PATH.exists():
        save_game()
        return get_state()

    data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
    saved_state = data.get("state", {})
    saved_logs = data.get("event_logs", [])

    next_state = _initial_state()
    if isinstance(saved_state, dict):
        next_state.update(saved_state)

    baekgyeong_state.clear()
    baekgyeong_state.update(next_state)

    event_logs.clear()
    if isinstance(saved_logs, list):
        event_logs.extend(saved_logs)

    return get_state()


load_game()
