from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Waypoint:
    x: float
    y: float
    z: Optional[float] = None

@dataclass(frozen=True)
class Mission:
    start_time: int
    end_time: int
    velocity: float
    waypoints: List[Waypoint]

@dataclass(frozen=True)
class DroneState:
    id: str
    controlled: bool
    paused: bool
    current_position: Waypoint
    mission: Optional[Mission] = None