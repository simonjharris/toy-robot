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
        self._point: Point | None = None
        self._direction: Direction | None = None
        self._is_placed = False

    @property
    def point(self) -> Point | None:
        return self._point

    @property
    def direction(self) -> Direction | None:
        return self._direction

    @property
    def is_placed(self) -> bool:
        return self._is_placed

    def place(self, point: Point, direction: Direction) -> None:
        self._point = point
        self._direction = direction
        self._is_placed = True

    def turn_left(self) -> None:
        if not self._is_placed:
            raise RobotNotPlacedError

        self._direction = self.anti_clockwise_rotations[self._direction]

    def turn_right(self) -> None:
        if not self._is_placed:
            raise RobotNotPlacedError

        self._direction = self.clockwise_rotations[self._direction]

    def move(self) -> None:
        if not self._is_placed:
            raise RobotNotPlacedError

        move_coordinate = self.move_coordinates[self._direction]
        new_position = Point(
            self._point.x + move_coordinate[0], self._point.y + move_coordinate[1]
        )
        self._point = new_position
