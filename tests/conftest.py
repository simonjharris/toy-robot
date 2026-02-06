import pytest

from toy_robot.data_classes import Direction, Point
from toy_robot.robot import Robot
from toy_robot.simulator import RobotSimulator
from toy_robot.table import Table


@pytest.fixture
def five_unit_square_table() -> Table:
    return Table(width=5, height=5)


@pytest.fixture
def centre_point_five_unit_table() -> Point:
    return Point(2, 2)


@pytest.fixture
def unplaced_robot() -> Robot:
    return Robot()


@pytest.fixture
def placed_robot_north_facing(
    unplaced_robot: Robot,
    centre_point_five_unit_table: Point,
) -> Robot:
    unplaced_robot.place(centre_point_five_unit_table, Direction.NORTH)
    return unplaced_robot


@pytest.fixture
def robot_simulator_unplaced_robot(
    unplaced_robot: Robot,
    five_unit_square_table: Table,
) -> RobotSimulator:
    return RobotSimulator(
        robot=unplaced_robot,
        table=five_unit_square_table,
    )


@pytest.fixture
def robot_simulator_placed_robot(
    placed_robot_north_facing: Robot,
    five_unit_square_table: Table,
) -> RobotSimulator:
    return RobotSimulator(
        robot=placed_robot_north_facing,
        table=five_unit_square_table,
    )
