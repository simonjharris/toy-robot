import pytest

from data_classes import Direction, Point
from robot import Robot
from table import Table


@pytest.fixture
def origin_point(robot: Robot) -> Point:
    return Point(0, 0)


@pytest.fixture
def robot():
    return Robot()


@pytest.fixture
def placed_robot_north_facing(robot: Robot, origin_point: Point) -> Robot:
    robot.place(origin_point, Direction.NORTH)
    return robot


@pytest.fixture
def five_unit_square_table() -> Table:
    return Table(width=5, height=5)
