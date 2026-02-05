import dataclasses
from enum import StrEnum


class Direction(StrEnum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: "Point | tuple[int, int]") -> bool:
        if isinstance(other, tuple):
            if len(other) != 2:
                return False
            return self.x == other[0] and self.y == other[1]
        else:
            return self.x == other.x and self.y == other.y
