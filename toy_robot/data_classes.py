import dataclasses
from enum import Enum, StrEnum, auto


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


@dataclasses.dataclass
class Point:
    x: int
    y: int
