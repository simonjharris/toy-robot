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
        self._point: Point | None = None
        self._direction: Direction | None = None

    def __str__(self) -> str:
        if self.point and self.direction:
            return f"{self.point.x},{self.point.y},{self.direction.name}"
        else:
            return "Unplaced Robot"

    @property
    def point(self) -> Point | None:
        return self._point

    @property
    def direction(self) -> Direction | None:
        return self._direction

    @property
    def is_placed(self) -> bool:
        return self._point is not None and self._direction is not None

    def place(self, point: Point, direction: Direction) -> None:
        self._point = point
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
        if self._point is None or self._direction is None:
            raise RobotNotPlacedError

        dx, dy = self.direction_deltas[self._direction]
        return Point(self._point.x + dx, self._point.y + dy)

    def move(self) -> None:
        self._point = self.next_position()
