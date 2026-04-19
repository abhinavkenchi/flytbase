from dataclasses import dataclass
from typing import List, Optional
import math

@dataclass(frozen=True)
class Waypoint:
    x: float
    y: float
    z: Optional[float] = None

@dataclass(frozen=True)
class Mission:
    start_time: float
    end_time: float
    velocity: float
    waypoints: tuple[Waypoint, ...]

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        if self.velocity <= 0:
            raise ValueError("velocity must be positive")
        if len(self.waypoints) < 2:
            raise ValueError("Need at least two waypoints")

        total_distance = 0.0
        previous = self.waypoints[0]
        for waypoint in self.waypoints[1:]:
            dx = waypoint.x - previous.x
            dy = waypoint.y - previous.y
            dz = (waypoint.z or 0.0) - (previous.z or 0.0)
            total_distance += math.hypot(dx, dy, dz)
            previous = waypoint

        required_time = total_distance / self.velocity
        mission_window = self.end_time - self.start_time
        if required_time > mission_window:
            raise ValueError(
                "Mission impossible: required time exceeds available mission window"
            )

@dataclass(frozen=True)
class DroneState:
    id: str
    controlled: bool
    paused: bool
    current_position: Waypoint
    mission: Optional[Mission] = None