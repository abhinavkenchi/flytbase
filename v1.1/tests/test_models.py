import pytest
from core.models import Waypoint, Mission

def test_valid_mission():
    m = Mission(
        start_time=0,
        end_time=10,
        velocity=1,
        waypoints=(Waypoint(0,0), Waypoint(10,0))
    )
    assert m.velocity == 1

def test_invalid_time():
    with pytest.raises(ValueError):
        Mission(
            start_time=10,
            end_time=5,
            velocity=1,
            waypoints=(Waypoint(0,0), Waypoint(1,1))
        )

def test_invalid_velocity():
    with pytest.raises(ValueError):
        Mission(
            start_time=0,
            end_time=5,
            velocity=0,
            waypoints=(Waypoint(0,0), Waypoint(1,1))
        )