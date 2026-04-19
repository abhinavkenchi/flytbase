from __future__ import annotations

from typing import Iterable, Tuple, List

from core.models import Mission, Waypoint


def _coordinates(point: Waypoint) -> Tuple[float, float, float]:
    x = float(point.x)
    y = float(point.y)
    z = float(point.z) if point.z is not None else 0.0
    return x, y, z


def euclidean_distance(p1: Waypoint, p2: Waypoint) -> float:
    x1, y1, z1 = _coordinates(p1)
    x2, y2, z2 = _coordinates(p2)

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


def path_length(waypoints: Iterable[Waypoint]) -> float:
    points = list(waypoints)

    if len(points) < 2:
        return 0.0

    total = 0.0

    for i in range(len(points) - 1):
        total += euclidean_distance(points[i], points[i + 1])

    return total


def segment_lengths(waypoints: Iterable[Waypoint]) -> List[float]:
    points = list(waypoints)

    if len(points) < 2:
        return []

    lengths = []

    for i in range(len(points) - 1):
        lengths.append(euclidean_distance(points[i], points[i + 1]))

    return lengths


def get_position_at_time(
    mission: Mission,
    t: float,
) -> Tuple[float, float, float]:

    waypoints = mission.waypoints

    if not waypoints:
        raise ValueError("Mission must contain at least one waypoint")

    if t <= mission.start_time:
        return _coordinates(waypoints[0])

    if t >= mission.end_time:
        return _coordinates(waypoints[-1])

    velocity = float(mission.velocity)

    if velocity <= 0:
        return _coordinates(waypoints[0])

    elapsed = t - mission.start_time
    travel_distance = elapsed * velocity

    seg_lengths = segment_lengths(waypoints)
    total_length = sum(seg_lengths)

    if total_length <= 0:
        return _coordinates(waypoints[0])

    travel_distance = min(travel_distance, total_length)

    for i, seg_len in enumerate(seg_lengths):
        if seg_len <= 0:
            continue

        if travel_distance <= seg_len:
            ratio = travel_distance / seg_len

            x1, y1, z1 = _coordinates(waypoints[i])
            x2, y2, z2 = _coordinates(waypoints[i + 1])

            return (
                x1 + ratio * (x2 - x1),
                y1 + ratio * (y2 - y1),
                z1 + ratio * (z2 - z1),
            )

        travel_distance -= seg_len

    return _coordinates(waypoints[-1])