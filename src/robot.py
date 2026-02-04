from data_classes import Direction, Point


class Robot:
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
            return

        rotations = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
        }
        self.direction = rotations[self.direction]

    def turn_right(self) -> None:
        if not self.is_placed:
            return

        rotations = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
        }

        self.direction = rotations[self.direction]

    def move(self) -> None:
        if not self.is_placed:
            return
