from dataclasses import dataclass, field
from threading import Lock
import time


@dataclass
class RuntimeState:
    drones: dict = field(default_factory=dict)
    paused: dict = field(default_factory=dict)

    safe_cycles: dict = field(default_factory=dict)
    cooldown: dict = field(default_factory=dict)
    pause_since: dict = field(default_factory=dict)

    events: list = field(default_factory=list)

    lock: Lock = field(default_factory=Lock)

    def log(self, msg):
        stamp = time.strftime("%H:%M:%S")
        self.events.insert(0, f"{stamp} | {msg}")
        self.events = self.events[:50]

    def update_drone(self, drone_id, drone):
        with self.lock:
            self.drones[drone_id] = drone

    def pause_drone(self, drone_id):
        with self.lock:
            if drone_id in self.drones:
                d = self.drones[drone_id]
                d["status"] = "paused"

                self.paused[drone_id] = d
                self.pause_since[drone_id] = time.time()
                self.safe_cycles[drone_id] = 0

                self.log(f"AUTO-PAUSED {drone_id}")

    def resume_drone(self, drone_id):
        with self.lock:
            if drone_id in self.drones:
                d = self.drones[drone_id]
                d["status"] = "flying"

            self.paused.pop(drone_id, None)
            self.pause_since.pop(drone_id, None)
            self.safe_cycles.pop(drone_id, None)

            self.cooldown[drone_id] = time.time()

            self.log(f"AUTO-RESUMED {drone_id}")