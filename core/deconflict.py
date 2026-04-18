from __future__ import annotations

from typing import Optional, Tuple, List
import math

from core.models import Mission
from core.trajectory import get_position_at_time


def overlapping_window(m1: Mission, m2: Mission) -> Optional[Tuple[float, float]]:
    start = max(m1.start_time, m2.start_time)
    end = min(m1.end_time, m2.end_time)
    return (start, end) if start < end else None


def severity_from_distance(distance: float, safety_distance: float) -> str:
    ratio = distance / safety_distance

    if ratio <= 0.4:
        return "high"
    if ratio <= 0.7:
        return "medium"
    return "low"


def predict_conflict(
    m1: Mission,
    m2: Mission,
    safety_distance: float = 5.0,
    time_step: float = 0.25,
) -> dict:
    if time_step <= 0:
        raise ValueError("time_step must be positive")

    window = overlapping_window(m1, m2)
    if window is None:
        return {"status": "clear"}

    start, end = window

    best_time = None
    best_distance = float("inf")
    best_a = None
    best_b = None

    t = start
    while t <= end:
        pos_a = get_position_at_time(m1, t)
        pos_b = get_position_at_time(m2, t)

        distance = math.dist(pos_a, pos_b)

        if distance < best_distance:
            best_distance = distance
            best_time = t
            best_a = pos_a
            best_b = pos_b

        t += time_step

    if best_distance <= safety_distance and best_time is not None:
        return {
            "status": "conflict",
            "conflict_time": round(best_time, 2),
            "distance": round(best_distance, 2),
            "position_a": best_a,
            "position_b": best_b,
            "severity": severity_from_distance(best_distance, safety_distance),
        }

    return {"status": "clear"}


def batch_check(
    primary_mission: Mission,
    other_missions: List[Mission],
    safety_distance: float = 5.0,
) -> List[dict]:
    results = []

    for mission in other_missions:
        result = predict_conflict(primary_mission, mission, safety_distance)
        if result["status"] == "conflict":
            results.append(result)

    return results