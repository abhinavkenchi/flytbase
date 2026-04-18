from __future__ import annotations
import math
from typing import Optional, Tuple, List

from core.models import Mission
from core.trajectory import get_position_at_time, euclidean_distance


def overlapping_window(m1: Mission, m2: Mission) -> Optional[Tuple[float, float]]:
    """Return the time window where both missions overlap, or None if they do not."""
    overlap_start = max(m1.start_time, m2.start_time)
    overlap_end = min(m1.end_time, m2.end_time)
    return (overlap_start, overlap_end) if overlap_start < overlap_end else None


def severity_from_distance(distance: float, safety_distance: float) -> str:
    """Return a severity level based on the distance."""
    if distance <= 0.4 * safety_distance:
        return "high"
    elif distance <= 0.7 * safety_distance:
        return "medium"
    else:
        return "low"


def predict_conflict(
    m1: Mission,
    m2: Mission,
    safety_distance: float = 5.0,
    time_step: float = 0.5,
) -> dict:
    """Predict the first conflict between two missions within their overlapping window."""
    if time_step <= 0.0:
        raise ValueError("time_step must be positive")

    window = overlapping_window(m1, m2)
    if window is None:
        return {"status": "clear"}

    start_time, end_time = window
    time = start_time
    while time <= end_time:
        position_a = get_position_at_time(m1, time)
        position_b = get_position_at_time(m2, time)
        distance = euclidean_distance(position_a, position_b)
        if distance <= safety_distance:
            return {
                "status": "conflict",
                "conflict_time": round(time, 2),
                "distance": round(distance, 2),
                "position_a": (position_a.x, position_a.y, position_a.z),
                "position_b": (position_b.x, position_b.y, position_b.z),
                "severity": severity_from_distance(distance, safety_distance),
            }
        time += time_step

    return {"status": "clear"}


def batch_check(primary_mission: Mission, other_missions: List[Mission], safety_distance: float = 5.0) -> List[dict]:
    """Check for conflicts between a primary mission and a list of other missions."""
    conflicts = []
    for m2 in other_missions:
        conflict = predict_conflict(primary_mission, m2, safety_distance)
        if conflict["status"] == "conflict":
            conflicts.append(conflict)
    return conflicts
