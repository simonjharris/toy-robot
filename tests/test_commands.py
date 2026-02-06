import pytest

from toy_robot.commands import (
    Command,
    CommandParser,
    InvalidCommandException,
    InvalidPlaceException,
    PlaceCommandArgs,
)
from toy_robot.data_classes import Direction


class TestCommandParser:
    @pytest.mark.parametrize(
        ["text_command", "expected_parsed_command"],
        [
            ["MOVE", (Command.MOVE, None)],
            [
                "MOVE ",
                (Command.MOVE, None),
            ],  # Not strictly in spec, but seems safe to allow
            ["REPORT", (Command.REPORT, None)],
            ["LEFT", (Command.LEFT, None)],
            ["RIGHT", (Command.RIGHT, None)],
            [
                "PLACE 1,1,NORTH",
                (Command.PLACE, PlaceCommandArgs(x=1, y=1, facing=Direction.NORTH)),
            ],
            [
                "PLACE 1, 1, SOUTH",  # spaces following
                (Command.PLACE, PlaceCommandArgs(x=1, y=1, facing=Direction.SOUTH)),
            ],
        ],
    )
    def test_parse_command_valid_returns_expected(
        self,
        text_command: str,
        expected_parsed_command: tuple[Command, PlaceCommandArgs | None],
    ) -> None:
        assert CommandParser.parse_command(text_command) == expected_parsed_command

    @pytest.mark.parametrize(
        "text_command",
        [
            "INVALID",
            "MOVER",
            "    REPORT",
            "left",
            "right",
            "FOO",
            "BAR",
        ],
    )
    def test_parse_command_invalid_raises_exception(self, text_command: str) -> None:
        with pytest.raises(InvalidCommandException):
            CommandParser.parse_command(text_command)

    @pytest.mark.parametrize(
        ["text_command", "expected_exception"],
        [
            ["PLACE", InvalidPlaceException],  # Missing required args
            ["PLACE X,Y,NORTH", InvalidPlaceException],  # Invalid arg type for point
            ["PLACE, 0,0,UP", InvalidPlaceException],  # Invalid arg type for direction
            [
                " PLACE 1,2,SOUTH",  # Leading whitespace, not recognised as PLACE
                InvalidCommandException,
            ],
        ],
    )
    def test_parse_command_place_invalid_raises_exception(
        self,
        text_command: str,
        expected_exception: type[Exception],
    ) -> None:
        with pytest.raises(expected_exception):
            CommandParser.parse_command(text_command)
