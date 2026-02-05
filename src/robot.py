from data_classes import Direction, Point


class RobotError(Exception):
    """Robot error base exception."""


class RobotNotPlacedError(RobotError):
    """Raised when attempting to operate a robot that has not been placed yet."""


class Robot:
    clockwise_rotations = {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST: Direction.NORTH,
    }
    anti_clockwise_rotations = {v: k for k, v in clockwise_rotations.items()}
    move_coordinates = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0),
    }

    def __init__(self):
        self.point: Point | None = None
        self.direction: Direction | None = None
        self.is_placed = False

    def place(self, point: Point, direction: Direction) -> None:
        self.point = point
        self.direction = direction
        self.is_placed = True

    def turn_left(self) -> None:
        if not self.is_placed:
            raise RobotNotPlacedError

        self.direction = self.anti_clockwise_rotations[self.direction]

    def turn_right(self) -> None:
        if not self.is_placed:
            raise RobotNotPlacedError

        self.direction = self.clockwise_rotations[self.direction]

    def move(self) -> None:
        if not self.is_placed:
            raise RobotNotPlacedError

        move_coordinate = self.move_coordinates[self.direction]
        new_position = Point(
            self.point.x + move_coordinate[0], self.point.y + move_coordinate[1]
        )
        self.point = new_position
