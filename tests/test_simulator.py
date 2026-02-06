import io

import pytest

from toy_robot.data_classes import Direction, Point
from toy_robot.simulator import RobotSimulator


class TestRobotSimulator:
    def test_process_command_move_success(
        self, robot_simulator_placed_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_placed_robot
        starting_position = simulator.robot.position
        next_position = simulator.robot.next_position()

        simulator.process_command("MOVE")

        new_position = simulator.robot.position
        assert new_position != starting_position
        assert new_position == next_position

    def test_process_command_not_placed_has_no_effect(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.position is None
        result = simulator.process_command("MOVE")
        assert result is None
        assert simulator.robot.position is None

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
        position = simulator.robot.position
        assert position is not None
        direction = simulator.robot.direction
        assert direction is not None
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
        assert simulator.robot.position == Point(0, 0)

    def test_process_command_replace_success(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        assert simulator.robot.is_placed is False
        simulator.process_command("PLACE 0,0,SOUTH")
        assert simulator.robot.is_placed is True
        assert simulator.robot.direction == Direction.SOUTH
        assert simulator.robot.position == Point(0, 0)
        simulator.process_command("PLACE 1,1,NORTH")
        assert simulator.robot.is_placed is True
        assert simulator.robot.direction == Direction.NORTH
        assert simulator.robot.position == Point(1, 1)

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

    @pytest.mark.parametrize(
        ["place_command", "expected_report"],
        [
            ["PLACE 0,4,NORTH", "0,4,NORTH"],  # north edge
            ["PLACE 4,0,EAST", "4,0,EAST"],  # east edge
            ["PLACE 0,0,SOUTH", "0,0,SOUTH"],  # south edge
            ["PLACE 0,0,WEST", "0,0,WEST"],  # west edge
        ],
    )
    def test_move_at_boundary_is_ignored(
        self,
        place_command: str,
        expected_report: str,
        robot_simulator_unplaced_robot: RobotSimulator,
    ) -> None:
        simulator = robot_simulator_unplaced_robot
        simulator.process_command(place_command)
        simulator.process_command("MOVE")
        assert simulator.process_command("REPORT") == expected_report


class TestCommandFileParser:
    def test_process_commands_example_c(
        self, robot_simulator_unplaced_robot: RobotSimulator
    ) -> None:
        """Problem spec example c: place, move, turn, move, report."""
        commands = "\n".join(
            [
                "PLACE 1,2,EAST",
                "MOVE",  # 2,2,EAST
                "MOVE",  # 3,2,EAST
                "LEFT",  # 3,2,NORTH
                "MOVE",  # 3,3,NORTH
                "REPORT",
            ]
        )
        file_like_input = io.StringIO(commands)
        simulator = robot_simulator_unplaced_robot
        result = simulator.process_commands(file_like_input)
        assert result == "3,3,NORTH"
