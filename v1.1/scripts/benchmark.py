from __future__ import annotations

import sys
from pathlib import Path

# -------------------------------------------------
# Add project root to Python path
# -------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import time
import random
import statistics
from typing import List, Dict

import pandas as pd

from core.dashboard_engine import detect_live_conflicts


AREA_MIN = 0.0
AREA_MAX = 20.0

SIZES = [10, 25, 50, 100, 200, 500]
RUNS_PER_CASE = 5


def generate_random_drones(n: int) -> List[Dict]:
    drones = []

    for i in range(n):
        drones.append(
            {
                "id": f"D{i+1}",
                "x": random.uniform(AREA_MIN, AREA_MAX),
                "y": random.uniform(AREA_MIN, AREA_MAX),
                "status": "active",
            }
        )

    return drones


def run_case(n: int, runs: int = RUNS_PER_CASE) -> Dict:
    timings = []
    alert_count = 0

    for _ in range(runs):
        drones = generate_random_drones(n)
        df = pd.DataFrame(drones)

        start = time.perf_counter()

        alerts, _, _ = detect_live_conflicts(df, tick=0)

        end = time.perf_counter()

        timings.append(end - start)
        alert_count = len(alerts)

    return {
        "drones": n,
        "pairs": (n * (n - 1)) // 2,
        "avg": statistics.mean(timings),
        "min": min(timings),
        "max": max(timings),
        "alerts": alert_count,
    }


if __name__ == "__main__":

    print("\nUAV Strategic Deconfliction Benchmark")
    print("=" * 78)

    for n in SIZES:
        r = run_case(n)

        print(
            f"{r['drones']:>4} drones | "
            f"{r['pairs']:>8} pairs | "
            f"avg {r['avg']:.6f}s | "
            f"min {r['min']:.6f}s | "
            f"max {r['max']:.6f}s | "
            f"alerts {r['alerts']}"
        )