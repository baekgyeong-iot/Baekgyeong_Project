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

DEFAULT_RANKINGS = {
    "blue_red_flag": [],
    "memory": [],
    "red_light_green_light": [],
}

GIFT_CATALOG = {
    1: {
        "name": "작은 조개껍데기",
        "description": "백경이가 주워온 작은 조개껍데기",
    },
    2: {
        "name": "반짝이는 유리조각",
        "description": "바닷가에서 발견한 반짝이는 유리조각",
    },
    3: {
        "name": "동글동글 조약돌",
        "description": "백경이가 마음에 들어 한 동그란 조약돌",
    },
}


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
        "sleep_check_requested": False,
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
inventory: list[dict[str, Any]] = []
rankings: dict[str, list[dict[str, Any]]] = deepcopy(DEFAULT_RANKINGS)


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


def get_inventory() -> list[dict[str, Any]]:
    return deepcopy(inventory)


def add_gift(gift_id: int) -> dict[str, Any]:
    catalog_item = GIFT_CATALOG.get(
        gift_id,
        {
            "name": f"알 수 없는 선물 {gift_id}",
            "description": "백경이가 가져온 정체불명의 선물",
        },
    )

    for gift in inventory:
        if gift["gift_id"] == gift_id:
            gift["count"] = int(gift.get("count", 0)) + 1
            gift["is_new"] = True
            gift["received_at"] = now_string()
            save_game()
            return deepcopy(gift)

    gift = {
        "gift_id": gift_id,
        "name": catalog_item["name"],
        "description": catalog_item["description"],
        "count": 1,
        "is_new": True,
        "received_at": now_string(),
    }
    inventory.append(gift)
    save_game()
    return deepcopy(gift)


def get_rankings() -> dict[str, list[dict[str, Any]]]:
    return deepcopy(rankings)


def add_ranking(game_type: str, score: int, date_string: str | None = None) -> dict[str, Any]:
    if game_type not in rankings:
        rankings[game_type] = []

    submitted_score = int(score)
    submitted_date = date_string or today_string()
    rankings[game_type].append(
        {
            "score": submitted_score,
            "date": submitted_date,
        }
    )
    rankings[game_type].sort(key=lambda item: int(item.get("score", 0)), reverse=True)

    ranked_items = []
    for index, item in enumerate(rankings[game_type], start=1):
        ranked_items.append(
            {
                "rank": index,
                "score": int(item.get("score", 0)),
                "date": item.get("date") or today_string(),
            }
        )
    submitted_entry = next(
        (
            item
            for item in ranked_items
            if item["score"] == submitted_score and item["date"] == submitted_date
        ),
        {
            "rank": None,
            "score": submitted_score,
            "date": submitted_date,
        },
    )
    rankings[game_type] = ranked_items[:3]
    save_game()
    return deepcopy(submitted_entry)


def state_updated_event() -> dict[str, Any]:
    return add_log("STATE_UPDATED", get_state())


def save_game() -> None:
    baekgyeong_state["last_saved_at"] = now_string()
    data = {
        "state": baekgyeong_state,
        "event_logs": event_logs[-100:],
        "inventory": inventory,
        "rankings": rankings,
    }
    SAVE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_game() -> dict[str, Any]:
    if not SAVE_PATH.exists():
        save_game()
        return get_state()

    data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
    saved_state = data.get("state", {})
    saved_logs = data.get("event_logs", [])
    saved_inventory = data.get("inventory", [])
    saved_rankings = data.get("rankings", {})

    next_state = _initial_state()
    if isinstance(saved_state, dict):
        next_state.update(saved_state)

    baekgyeong_state.clear()
    baekgyeong_state.update(next_state)

    event_logs.clear()
    if isinstance(saved_logs, list):
        event_logs.extend(saved_logs)

    inventory.clear()
    if isinstance(saved_inventory, list):
        inventory.extend(saved_inventory)

    rankings.clear()
    rankings.update(deepcopy(DEFAULT_RANKINGS))
    if isinstance(saved_rankings, dict):
        for game_type, entries in saved_rankings.items():
            if isinstance(entries, list):
                rankings[game_type] = entries

    return get_state()


load_game()
