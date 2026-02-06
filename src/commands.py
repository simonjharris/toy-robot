import dataclasses
import re
from enum import StrEnum

from src.data_classes import Direction


class CommandParserException(Exception):
    pass


class InvalidCommandException(CommandParserException):
    pass


class InvalidPlaceException(CommandParserException):
    pass


class Command(StrEnum):
    PLACE = "PLACE"
    MOVE = "MOVE"
    REPORT = "REPORT"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    EXIT = "EXIT"


@dataclasses.dataclass
class PlaceCommandArgs:
    x: int
    y: int
    facing: Direction


class CommandParser:
    place_command_regex = re.compile(
        r"^PLACE\s([0-9]+),\s?([0-9]+),\s?(NORTH|EAST|SOUTH|WEST)$",
    )

    @classmethod
    def _parse_place_command_args(cls, command: str) -> PlaceCommandArgs:
        if not (match := re.match(cls.place_command_regex, command)):
            raise InvalidPlaceException

        x = int(match.group(1))
        y = int(match.group(2))
        direction = Direction[match.group(3).upper()]
        return PlaceCommandArgs(x, y, direction)

    @classmethod
    def parse_command(cls, command: str) -> tuple[Command, PlaceCommandArgs | None]:
        command_type = command.split(" ")[0]

        if command_type in ("MOVE", "REPORT", "LEFT", "RIGHT", "EXIT"):
            return Command[command_type], None

        if not command_type.startswith("PLACE"):
            raise InvalidCommandException

        return Command.PLACE, cls._parse_place_command_args(command)
