import pytest

from toy_robot.data_classes import Direction, Point
from toy_robot.robot import Robot, RobotNotPlacedError


class TestRobot:
    def test_move_alters_position_correctly(
        self, placed_robot_north_facing: Robot, centre_point_five_unit_table: Point
    ) -> None:
        assert placed_robot_north_facing.direction == Direction.NORTH

        placed_robot_north_facing.move()
        assert placed_robot_north_facing.point == Point(
            centre_point_five_unit_table.x, centre_point_five_unit_table.y + 1
        )
        assert placed_robot_north_facing.direction == Direction.NORTH

    def test_clockwise_circle_returns_to_origin(
        self, placed_robot_north_facing: Robot
    ) -> None:
        """Test that after a full CW circle (4 moves and 4 turns)
        the robot is in the same state as when starting
        """
        robot = placed_robot_north_facing
        starting_point = robot.point
        commands_to_return_to_starting_point = [robot.move, robot.turn_right] * 4
        expected_position_offset = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]

        path = [starting_point]
        for command in commands_to_return_to_starting_point:
            command()
            if path[-1] != robot.point:
                path.append(robot.point)

        assert placed_robot_north_facing.direction == Direction.NORTH
        assert path == [
            Point(starting_point.x + dx_dy[0], starting_point.y + dx_dy[1])
            for dx_dy in expected_position_offset
        ]

    def test_anti_clockwise_circle_returns_to_origin(
        self, placed_robot_north_facing: Robot
    ) -> None:
        """Test that after a full ACW circle (4 moves and 4 turns)
        the robot is in the same state as when starting
        """
        robot = placed_robot_north_facing
        starting_point = robot.point
        commands_to_return_to_starting_point = [robot.move, robot.turn_left] * 4
        expected_position_offset = [(0, 0), (0, 1), (-1, 1), (-1, 0), (0, 0)]

        path = [starting_point]
        for command in commands_to_return_to_starting_point:
            command()
            if path[-1] != robot.point:
                path.append(robot.point)

        assert placed_robot_north_facing.direction == Direction.NORTH
        assert path == [
            Point(starting_point.x + dx_dy[0], starting_point.y + dx_dy[1])
            for dx_dy in expected_position_offset
        ]

    def test_next_position_returns_candidate_without_mutating(
        self, placed_robot_north_facing: Robot
    ) -> None:
        candidate = placed_robot_north_facing.next_position()
        starting_position = placed_robot_north_facing.point
        assert candidate == Point(starting_position.x, starting_position.y + 1)
        assert placed_robot_north_facing.point == starting_position

    def test_unplaced_robot_raises_error_on_move(self, unplaced_robot: Robot) -> None:
        with pytest.raises(RobotNotPlacedError):
            unplaced_robot.move()

    def test_unplaced_robot_raises_on_turn_left(self, unplaced_robot: Robot) -> None:
        with pytest.raises(RobotNotPlacedError):
            unplaced_robot.turn_left()

    def test_unplaced_robot_raises_on_turn_right(self, unplaced_robot: Robot) -> None:
        with pytest.raises(RobotNotPlacedError):
            unplaced_robot.turn_right()

    def test_unplaced_robot_raises_on_next_position(
        self, unplaced_robot: Robot
    ) -> None:
        with pytest.raises(RobotNotPlacedError):
            unplaced_robot.next_position()

    def test_robot_is_placed(self, unplaced_robot: Robot) -> None:
        robot = unplaced_robot
        assert unplaced_robot.is_placed is False
        robot.place(Point(0, 0), Direction.NORTH)
        assert unplaced_robot.is_placed is True

    def test_robot_string_representation(self, unplaced_robot: Robot) -> None:
        robot = unplaced_robot
        assert str(robot) == "Unplaced Robot"
        robot.place(Point(0, 0), Direction.NORTH)
        assert str(robot) == "0,0,NORTH"
