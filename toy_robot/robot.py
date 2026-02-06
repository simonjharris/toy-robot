from toy_robot.data_classes import Direction, Point


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
    anti_clockwise_rotations = {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.NORTH,
    }
    direction_deltas = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0),
    }

    def __init__(self) -> None:
        self._position: Point | None = None
        self._direction: Direction | None = None

    def __str__(self) -> str:
        if self.position is not None and self.direction is not None:
            return f"{self.position.x},{self.position.y},{self.direction.name}"
        else:
            return "Unplaced Robot"

    @property
    def position(self) -> Point | None:
        return self._position

    @property
    def direction(self) -> Direction | None:
        return self._direction

    @property
    def is_placed(self) -> bool:
        return self._position is not None and self._direction is not None

    def place(self, position: Point, direction: Direction) -> None:
        self._position = position
        self._direction = direction

    def turn_left(self) -> None:
        if self._direction is None:
            raise RobotNotPlacedError

        self._direction = self.anti_clockwise_rotations[self._direction]

    def turn_right(self) -> None:
        if self._direction is None:
            raise RobotNotPlacedError

        self._direction = self.clockwise_rotations[self._direction]

    def next_position(self) -> Point:
        if self._position is None or self._direction is None:
            raise RobotNotPlacedError

        dx, dy = self.direction_deltas[self._direction]
        return Point(self._position.x + dx, self._position.y + dy)

    def move(self) -> None:
        self._position = self.next_position()
