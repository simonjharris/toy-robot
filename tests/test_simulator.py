import pytest

from src.data_classes import Direction, Point
from src.simulator import RobotSimulator


class TestRobotSimulator:
    def test_process_line_move_success(
        self, robot_simulator_placed_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_placed_robot
        starting_position = simulator.robot.point
        next_position = simulator.robot.next_position()

        simulator.process_line("MOVE")

        new_position = simulator.robot.point
        assert new_position != starting_position
        assert new_position == next_position

    def test_process_line_not_placed_has_no_effect(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.point is None
        result = simulator.process_line("MOVE")
        assert result is None
        assert simulator.robot.point is None

    @pytest.mark.parametrize(
        ["text_command", "expected_facing_direction"],
        [
            ["LEFT", Direction.WEST],
            ["RIGHT", Direction.EAST],
        ],
    )
    def test_process_line_left_right_success(
        self,
        text_command: str,
        expected_facing_direction: Direction,
        robot_simulator_placed_robot: RobotSimulator,
    ) -> None:
        simulator = robot_simulator_placed_robot
        simulator.robot._direction = Direction.NORTH
        simulator.process_line(text_command)
        assert simulator.robot.direction == expected_facing_direction

    @pytest.mark.parametrize(
        "text_command",
        ["LEFT", "RIGHT"],
    )
    def test_process_line_left_right_not_placed_has_no_effect(
        self, text_command: str, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.direction is None
        simulator.process_line(text_command)
        assert simulator.robot.direction is None

    def test_process_line_report_success(
        self, robot_simulator_placed_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_placed_robot
        position = simulator.robot.point
        direction = simulator.robot.direction
        output = simulator.process_line("REPORT")
        assert output == f"{position.x},{position.y},{direction.name}"

    def test_process_line_report_not_placed_has_no_effect(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        output = simulator.process_line("REPORT")
        assert output is None

    def test_process_line_place_success(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.is_placed is False
        simulator.process_line("PLACE 0,0,SOUTH")
        assert simulator.robot.is_placed is True
        assert simulator.robot.direction == Direction.SOUTH
        assert simulator.robot.point == Point(0, 0)

    @pytest.mark.parametrize("invalid_place_command", ["PLACE X,Y,INVALID", "PLACE"])
    def test_process_line_invalid_has_no_effect(
        self,
        invalid_place_command: str,
        robot_simulator_unplaced_robot: RobotSimulator,
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.is_placed is False
        simulator.process_line(invalid_place_command)
        assert simulator.robot.is_placed is False

    def test_process_line_exit_success(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        with pytest.raises(SystemExit):
            simulator.process_line("EXIT")
