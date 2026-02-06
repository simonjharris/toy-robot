import io

import pytest

from toy_robot.data_classes import Direction, Point
from toy_robot.simulator import RobotSimulator, Signal


class TestRobotSimulator:
    def test_process_command_move_success(
        self, robot_simulator_placed_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_placed_robot
        starting_position = simulator.robot.point
        next_position = simulator.robot.next_position()

        simulator.process_command("MOVE")

        new_position = simulator.robot.point
        assert new_position != starting_position
        assert new_position == next_position

    def test_process_command_not_placed_has_no_effect(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.point is None
        result = simulator.process_command("MOVE")
        assert result is None
        assert simulator.robot.point is None

    @pytest.mark.parametrize(
        ["text_command", "expected_facing_direction"],
        [
            ["LEFT", Direction.WEST],
            ["RIGHT", Direction.EAST],
        ],
    )
    def test_process_command_left_right_success(
        self,
        text_command: str,
        expected_facing_direction: Direction,
        robot_simulator_unplaced_robot: RobotSimulator,
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        simulator.process_command("PLACE 0,0,NORTH")
        simulator.process_command(text_command)
        assert simulator.robot.direction == expected_facing_direction

    @pytest.mark.parametrize(
        "text_command",
        ["LEFT", "RIGHT"],
    )
    def test_process_command_left_right_not_placed_has_no_effect(
        self, text_command: str, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.direction is None
        simulator.process_command(text_command)
        assert simulator.robot.direction is None

    def test_process_command_report_success(
        self, robot_simulator_placed_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_placed_robot
        position = simulator.robot.point
        direction = simulator.robot.direction
        output = simulator.process_command("REPORT")
        assert output == f"{position.x},{position.y},{direction.name}"

    def test_process_command_report_not_placed_has_no_effect(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        output = simulator.process_command("REPORT")
        assert output is None

    def test_process_command_place_success(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.is_placed is False
        simulator.process_command("PLACE 0,0,SOUTH")
        assert simulator.robot.is_placed is True
        assert simulator.robot.direction == Direction.SOUTH
        assert simulator.robot.point == Point(0, 0)

    @pytest.mark.parametrize("invalid_place_command", ["PLACE X,Y,INVALID", "PLACE"])
    def test_process_command_invalid_has_no_effect(
        self,
        invalid_place_command: str,
        robot_simulator_unplaced_robot: RobotSimulator,
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.is_placed is False
        simulator.process_command(invalid_place_command)
        assert simulator.robot.is_placed is False

    def test_process_command_exit_success(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.process_command("EXIT") is Signal.EXIT


class TestCommandFileParser:
    def test_process_commands(self, robot_simulator_unplaced_robot):
        commands = "\n".join(
            [
                "REPORT",  # ignored - robot not yet placed
                "PLACE 1,1,SOUTH",
                "MOVE",  # 1,0,SOUTH
                "RIGHT",  # 1,0,WEST
                "MOVE",  # 0,0,WEST
                "REPORT",  # outputs "0,0,WEST"
            ]
        )
        file_like_input = io.StringIO(commands)
        simulator = robot_simulator_unplaced_robot
        result = simulator.process_commands(file_like_input)
        assert result == "0,0,WEST"
