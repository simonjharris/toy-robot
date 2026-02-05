import pytest

from data_classes import Direction, Point
from robot import Robot
from table import Table


@pytest.fixture
def centre_point(robot: Robot) -> Point:
    return Point(2, 2)


@pytest.fixture
def robot():
    return Robot()


@pytest.fixture
def placed_robot_north_facing(robot: Robot, centre_point: Point) -> Robot:
    robot.place(centre_point, Direction.NORTH)
    return robot


@pytest.fixture
def five_unit_square_table() -> Table:
    return Table(width=5, height=5)
