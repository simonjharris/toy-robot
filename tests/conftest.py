import pytest

from src.data_classes import Direction, Point
from src.robot import Robot
from src.table import Table


@pytest.fixture
def five_unit_square_table() -> Table:
    return Table(width=5, height=5)


@pytest.fixture
def centre_point_five_unit_table() -> Point:
    return Point(2, 2)


@pytest.fixture
def unplaced_robot():
    return Robot()


@pytest.fixture
def placed_robot_north_facing(
    unplaced_robot: Robot,
    centre_point_five_unit_table: Point,
) -> Robot:
    unplaced_robot.place(centre_point_five_unit_table, Direction.NORTH)
    return unplaced_robot
