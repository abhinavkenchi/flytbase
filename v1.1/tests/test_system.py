import pytest

from core.models import Waypoint, Mission
from core.deconflict import (
    predict_conflict,
    overlapping_window,
    batch_check,
)


def test_clear_mission():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(5, 0),
        ),
    )

    m2 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 10),
            Waypoint(5, 10),
        ),
    )

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "clear"


def test_conflict_mission():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 10),
        ),
    )

    m2 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 10),
            Waypoint(10, 0),
        ),
    )

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "conflict"


def test_no_time_overlap():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 10),
        ),
    )

    m2 = Mission(
        30, 50, 1,
        (
            Waypoint(0, 10),
            Waypoint(10, 0),
        ),
    )

    assert overlapping_window(m1, m2) is None

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "clear"


def test_impossible_mission():
    with pytest.raises(ValueError):
        Mission(
            0, 5, 1,
            (
                Waypoint(0, 0),
                Waypoint(100, 100),
            ),
        )


def test_boundary_distance():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(5, 0),
        ),
    )

    m2 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 1.5),
            Waypoint(5, 1.5),
        ),
    )

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "conflict"


def test_multi_waypoint_valid():
    mission = Mission(
        0, 80, 2,
        (
            Waypoint(0, 5),
            Waypoint(20, 8),
            Waypoint(30, 50),
            Waypoint(35, 70),
        ),
    )

    assert mission.velocity == 2
    assert len(mission.waypoints) == 4


def test_zero_velocity():
    with pytest.raises(ValueError):
        Mission(
            0, 20, 0,
            (
                Waypoint(0, 0),
                Waypoint(10, 10),
            ),
        )


def test_identical_path():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 10),
        ),
    )

    m2 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 10),
        ),
    )

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "conflict"


def test_touching_safety_radius():
    m1 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 0),
        ),
    )

    m2 = Mission(
        0, 20, 1,
        (
            Waypoint(0, 1.5),
            Waypoint(10, 1.5),
        ),
    )

    result = predict_conflict(m1, m2, 1.5)

    assert result["status"] == "conflict"


def test_many_drones():
    primary = Mission(
        0, 20, 1,
        (
            Waypoint(0, 0),
            Waypoint(10, 10),
        ),
    )

    others = [
        Mission(
            0, 20, 1,
            (
                Waypoint(0, 10),
                Waypoint(10, 0),
            ),
        ),
        Mission(
            0, 20, 1,
            (
                Waypoint(20, 20),
                Waypoint(30, 30),
            ),
        ),
        Mission(
            5, 25, 1,
            (
                Waypoint(2, 0),
                Waypoint(8, 10),
            ),
        ),
        Mission(
            0, 20, 1,
            (
                Waypoint(-5, -5),
                Waypoint(-10, -10),
            ),
        ),
    ]

    results = batch_check(primary, others, 1.5)

    assert isinstance(results, list)
    assert len(results) >= 1