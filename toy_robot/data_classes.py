import dataclasses
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
