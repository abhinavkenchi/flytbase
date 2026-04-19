import random

def spawn_drones(n=30):
    drones = []

    for i in range(n):
        drones.append({
            "id": f"C{i}" if i < 20 else f"U{i}",
            "type": "controlled" if i < 20 else "unknown",
            "x": random.randint(0, 100),
            "y": random.randint(0, 100),
            "vx": random.uniform(-2, 2),
            "vy": random.uniform(-2, 2),
            "status": "flying"
        })

    return drones