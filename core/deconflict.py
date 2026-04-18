from __future__ import annotations
import math
from typing import Optional, Tuple

from core.models import Mission
from core.trajectory import get_position_at_time


def overlapping_window(m1: Mission, m2: Mission) -> Optional[Tuple[float, float]]:
    """Return the time window where both missions overlap, or None if they do not."""
    overlap_start = max(m1.start_time, m2.start_time)
    overlap_end = min(m1.end_time, m2.end_time)
    return (overlap_start, overlap_end) if overlap_start < overlap_end else None


def severity_from_distance(distance: float, safety_distance: float) -> float:
    """Return a severity score from 0.0 (safe) to 1.0 (collision threat)."""
    if distance <= 0.0:
        return 1.0
    if distance >= safety_distance:
        return 0.0
    return (safety_distance - distance) / safety_distance


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
        distance = math.dist(position_a, position_b)
        if distance <= safety_distance:
            return {
                "status": "conflict",
                "conflict_time": time,
                "distance": distance,
                "position_a": position_a,
                "position_b": position_b,
                "severity": severity_from_distance(distance, safety_distance),
            }
        time += time_step

    return {"status": "clear"}
