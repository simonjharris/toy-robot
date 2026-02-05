from data_classes import Direction, Point
from robot import Robot


class TestRobot:
    def test_move_alters_position_correctly(self, placed_robot_north_facing: Robot):
        assert placed_robot_north_facing.point == (0, 0)
        assert placed_robot_north_facing.direction == Direction.NORTH

        placed_robot_north_facing.move()
        assert placed_robot_north_facing.point == (0, 1)
        assert placed_robot_north_facing.direction == Direction.NORTH

    def test_clockwise_circle_returns_to_origin(self, placed_robot_north_facing: Robot):
        robot = placed_robot_north_facing
        origin_point = robot.point
        commands_to_return_to_origin = [robot.move, robot.turn_right] * 4

        path = [origin_point]
        for command in commands_to_return_to_origin:
            command()
            if path[-1] != robot.point:
                path.append(robot.point)

        assert placed_robot_north_facing.point == (0, 0)
        assert placed_robot_north_facing.direction == Direction.NORTH
        assert path == [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]

    def test_anti_clockwise_circle_returns_to_origin(
        self, placed_robot_north_facing: Robot
    ):
        robot = placed_robot_north_facing
        origin_point = robot.point
        commands_to_return_to_origin = [robot.move, robot.turn_left] * 4

        path = [origin_point]
        for command in commands_to_return_to_origin:
            command()
            if path[-1] != robot.point:
                path.append(robot.point)

        assert placed_robot_north_facing.point == Point(0, 0)
        assert placed_robot_north_facing.direction == Direction.NORTH
        assert path == [(0, 0), (0, 1), (-1, 1), (-1, 0), (0, 0)]
