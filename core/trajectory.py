from __future__ import annotations
from typing import Iterable, Tuple

from core.models import Mission, Waypoint


def _coordinates(point: Waypoint) -> Tuple[float, float, float]:
    x = float(point.x)
    y = float(point.y)
    z = point.z
    return x, y, float(z) if z is not None else 0.0


def euclidean_distance(p1: Waypoint, p2: Waypoint) -> float:
    """Return the 3D Euclidean distance between two points."""
    x1, y1, z1 = _coordinates(p1)
    x2, y2, z2 = _coordinates(p2)
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5


def path_length(waypoints: Iterable[Waypoint]) -> float:
    """Return total path length defined by a sequence of waypoints."""
    waypoints = list(waypoints)
    if len(waypoints) < 2:
        return 0.0

    distance = 0.0
    previous = waypoints[0]
    for waypoint in waypoints[1:]:
        distance += euclidean_distance(previous, waypoint)
        previous = waypoint
    return distance


def get_position_at_time(mission: Mission, t: float) -> Tuple[float, float, float]:
    """Return interpolated x,y,z along mission waypoints at time t.

    Assumes constant velocity along the waypoint segments.
    """
    waypoints = mission.waypoints
    if not waypoints:
        raise ValueError("Mission must contain at least one waypoint")

    if t <= mission.start_time:
        return _coordinates(waypoints[0])

    if t >= mission.end_time:
        return _coordinates(waypoints[-1])

    velocity = float(mission.velocity)
    if velocity <= 0.0:
        return _coordinates(waypoints[0])

    elapsed = float(t - mission.start_time)
    target_distance = elapsed * velocity
    total_distance = path_length(waypoints)
    if total_distance <= 0.0:
        return _coordinates(waypoints[0])

    target_distance = min(target_distance, total_distance)
    previous = waypoints[0]

    for waypoint in waypoints[1:]:
        segment_length = euclidean_distance(previous, waypoint)
        if segment_length <= 0.0:
            previous = waypoint
            continue

        if target_distance <= segment_length:
            ratio = target_distance / segment_length
            x1, y1, z1 = _coordinates(previous)
            x2, y2, z2 = _coordinates(waypoint)
            return (
                x1 + ratio * (x2 - x1),
                y1 + ratio * (y2 - y1),
                z1 + ratio * (z2 - z1),
            )

        target_distance -= segment_length
        previous = waypoint

    return _coordinates(waypoints[-1])
