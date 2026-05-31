from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from . import logic, state
except ImportError:
    import logic  # type: ignore
    import state  # type: ignore


@dataclass(frozen=True)
class EvolutionRule:
    from_stage: str
    to_stage: str
    required_days: int
    required_count: int


EVOLUTION_RULES: dict[str, EvolutionRule] = {
    state.STAGE_BABY: EvolutionRule(state.STAGE_BABY, state.STAGE_CHILD, 1, 2),
    state.STAGE_CHILD: EvolutionRule(state.STAGE_CHILD, state.STAGE_ADULT, 3, 5),
}


def get_rule(growth_stage: str | None = None) -> EvolutionRule | None:
    stage = growth_stage or state.baekgyeong_state["growth_stage"]
    return EVOLUTION_RULES.get(stage)


def can_evolve(date_string: str | None = None) -> bool:
    current = state.baekgyeong_state
    rule = get_rule(current["growth_stage"])
    if rule is None:
        return False

    alive_days = logic.days_between(current["birth_date"], date_string)
    return (
        alive_days >= rule.required_days
        and current["feed_count"] >= rule.required_count
        and current["play_count"] >= rule.required_count
        and current["sleep_count"] >= rule.required_count
    )


def check_evolution(trigger: str = "action_performed", date_string: str | None = None) -> dict[str, Any]:
    current_date = date_string or state.today_string()
    current = state.baekgyeong_state
    payload = {
        "birth_date": current["birth_date"],
        "date": current_date,
        "feed_count": current["feed_count"],
        "play_count": current["play_count"],
        "sleep_count": current["sleep_count"],
        "growth_stage": current["growth_stage"],
        "trigger": trigger,
    }
    state.add_log("EVO_CHECK", payload)

    if can_evolve(current_date):
        return evolve(current_date)
    return state.make_event("SYSTEM", "EVO_CHECK_RESULT", {**payload, "can_evolve": False})


def evolve(date_string: str | None = None) -> dict[str, Any]:
    current = state.baekgyeong_state
    rule = get_rule(current["growth_stage"])
    if rule is None:
        return state.add_log(
            "EVO_EVENT_SKIPPED",
            {"reason": "already_final_stage", "growth_stage": current["growth_stage"]},
        )

    from_stage = current["growth_stage"]
    current["growth_stage"] = rule.to_stage
    logic.refresh_mood()
    return state.add_log(
        "EVO_EVENT_TRIGGERED",
        {
            "from_stage": from_stage,
            "to_stage": rule.to_stage,
            "date": date_string or state.today_string(),
        },
    )
