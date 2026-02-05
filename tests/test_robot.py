from data_classes import Direction, Point
from robot import Robot


class TestRobot:
    def test_move_alters_position_correctly(
        self, placed_robot_north_facing: Robot, centre_point: Point
    ) -> None:
        assert placed_robot_north_facing.direction == Direction.NORTH

        placed_robot_north_facing.move()
        assert placed_robot_north_facing.point == Point(
            centre_point.x, centre_point.y + 1
        )
        assert placed_robot_north_facing.direction == Direction.NORTH

    def test_clockwise_circle_returns_to_origin(self, placed_robot_north_facing: Robot):
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
            Point(starting_point.x + xy_offset[0], starting_point.y + xy_offset[1])
            for xy_offset in expected_position_offset
        ]

    def test_anti_clockwise_circle_returns_to_origin(
        self, placed_robot_north_facing: Robot
    ):
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
            Point(starting_point.x + xy_offset[0], starting_point.y + xy_offset[1])
            for xy_offset in expected_position_offset
        ]
