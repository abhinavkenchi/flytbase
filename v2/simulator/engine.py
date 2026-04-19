import time

from simulator.controlled import update_controlled
from simulator.unknown import update_unknown


class SimEngine:
    def __init__(self, drones, state):
        self.drones = drones
        self.state = state
        self.running = False

    def tick(self, dt=1.0):
        for drone in self.drones:

            if drone["type"] == "controlled":
                update_controlled(drone, dt)
            else:
                update_unknown(drone, dt)

            self.state.update_drone(drone["id"], drone)

    def run(self, dt=1.0):
        self.running = True

        while self.running:
            self.tick(dt)
            time.sleep(dt)

    def stop(self):
        self.running = False