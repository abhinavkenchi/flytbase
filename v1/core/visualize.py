from __future__ import annotations

from typing import Sequence, Optional
import numpy as np
import matplotlib.pyplot as plt

from core.models import Mission
from core.trajectory import get_position_at_time


def extract_xy(points):
    return [p[0] for p in points], [p[1] for p in points]


def sample_mission(mission: Mission, samples: int = 80):
    times = np.linspace(mission.start_time, mission.end_time, samples)
    return [get_position_at_time(mission, t) for t in times]


def finalize_plot(title: str, save_path: Optional[str], show_plot: bool):
    plt.title(title, fontsize=14)
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=220, bbox_inches="tight")

    if show_plot:
        plt.show()
    else:
        plt.close()


def plot_mission_paths(
    missions: Sequence[Mission],
    labels=None,
    title="Mission Paths",
    save_path=None,
    show_plot=True,
):
    plt.figure(figsize=(10, 6))

    for i, mission in enumerate(missions):
        pts = sample_mission(mission)
        xs, ys = extract_xy(pts)

        label = labels[i] if labels else f"Drone {i+1}"

        plt.plot(xs, ys, linewidth=2, label=label)
        plt.scatter(xs[0], ys[0], color="green", s=60)
        plt.scatter(xs[-1], ys[-1], color="red", marker="X", s=80)

    finalize_plot(title, save_path, show_plot)


def plot_two_missions_with_conflict(
    m1,
    m2,
    conflict_result,
    save_path=None,
    show_plot=True,
):
    plt.figure(figsize=(10, 6))

    missions = [(m1, "Primary"), (m2, "Other")]

    for mission, label in missions:
        pts = sample_mission(mission)
        xs, ys = extract_xy(pts)

        plt.plot(xs, ys, linewidth=2, label=label)
        plt.scatter(xs[0], ys[0], color="green", s=60)
        plt.scatter(xs[-1], ys[-1], color="red", marker="X", s=80)

    if conflict_result["status"] == "conflict":
        pa = conflict_result["position_a"]
        pb = conflict_result["position_b"]

        cx = (pa[0] + pb[0]) / 2
        cy = (pa[1] + pb[1]) / 2

        plt.scatter(cx, cy, marker="*", s=260, color="red", label="Conflict")

        plt.annotate(
            f'T={conflict_result["conflict_time"]}s\n{conflict_result["severity"]}',
            (cx, cy),
            xytext=(cx + 0.6, cy + 0.6)
        )

    plt.title("UAV Strategic Deconfliction - Conflict Scenario")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=220)

    if show_plot:
        plt.show()
    else:
        plt.close()