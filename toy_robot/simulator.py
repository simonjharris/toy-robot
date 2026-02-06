from typing import TextIO

from toy_robot.commands import (
    Command,
    CommandParser,
    CommandParserException,
    PlaceCommandArgs,
)
from toy_robot.data_classes import Point
from toy_robot.robot import Robot, RobotNotPlacedError
from toy_robot.table import Table


class RobotSimulator:
    def __init__(self, robot: Robot, table: Table):
        self.robot = robot
        self.table = table

    def _execute(
        self, command: Command, place_args: PlaceCommandArgs | None = None
    ) -> str | None:
        match command:
            case Command.PLACE:
                self._handle_place(place_args)
            case Command.MOVE:
                self._handle_move()
            case Command.LEFT:
                self._handle_left()
            case Command.RIGHT:
                self._handle_right()
            case Command.REPORT:
                return self._handle_report()
        return None

    def _handle_place(self, args: PlaceCommandArgs | None) -> None:
        if args is None:
            return
        point = Point(args.x, args.y)
        if self.table.is_valid_point(point):
            self.robot.place(point, args.facing)

    def _handle_move(self) -> None:
        try:
            candidate_position = self.robot.next_position()
            if self.table.is_valid_point(candidate_position):
                self.robot.move()
        except RobotNotPlacedError:
            return None

    def _handle_left(self) -> None:
        try:
            self.robot.turn_left()
        except RobotNotPlacedError:
            return None

    def _handle_right(self) -> None:
        try:
            self.robot.turn_right()
        except RobotNotPlacedError:
            return None

    def _handle_report(self) -> str | None:
        return str(self.robot) if self.robot.is_placed else None

    def process_command(self, line: str) -> str | None:
        try:
            command, place_args = CommandParser.parse_command(line.rstrip())
            return self._execute(command, place_args)
        except CommandParserException:
            return None

    def process_commands(self, file_contents: TextIO) -> str | None:
        output_lines = []
        for line in file_contents:
            result = self.process_command(line)
            if result is not None:
                output_lines.append(result)

        return "\n".join(output_lines) if output_lines else None
