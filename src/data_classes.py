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
