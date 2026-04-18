import math
from typing import List, Dict


def generate_drones(tick: int) -> List[Dict]:
    drones = []

    drones.append({
        "id": "Drone_1",
        "x": tick % 20,
        "y": tick % 20,
        "status": "ACTIVE"
    })

    drones.append({
        "id": "Drone_2",
        "x": 20 - (tick % 20),
        "y": tick % 20,
        "status": "ACTIVE"
    })

    drones.append({
        "id": "Drone_3",
        "x": 10 + 5 * math.sin(tick / 2),
        "y": 10 + 5 * math.cos(tick / 2),
        "status": "ACTIVE"
    })

    drones.append({
        "id": "Drone_4",
        "x": 5,
        "y": (tick * 1.5) % 20,
        "status": "ACTIVE"
    })

    drones.append({
        "id": "Drone_5",
        "x": (tick * 1.2) % 20,
        "y": 15,
        "status": "ACTIVE"
    })

    return drones