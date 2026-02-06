import subprocess
import sys
from unittest.mock import patch

import pytest

from main import main


class TestInteractiveMode:
    @patch("builtins.input", side_effect=["PLACE 1,2,NORTH", "MOVE", "REPORT", "EXIT"])
    @patch("sys.argv", ["main"])
    def test_process_commands_and_report(self, mock_input, capsys):
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "1,3,NORTH" in captured.out

    @patch("builtins.input", side_effect=["EXIT"])
    @patch("sys.argv", ["main"])
    def test_exit_command(self, mock_input):
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

    @patch("builtins.input", side_effect=["EXIT"])
    @patch("sys.argv", ["main"])
    def test_welcome_message(self, mock_input, capsys):
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Welcome to the Robot Simulator" in captured.out


class TestHelp:
    @patch("sys.argv", ["main", "--help"])
    def test_help_flag(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "PLACE" in captured.out
        assert "REPORT" in captured.out


class TestFileMode:
    def test_process_command_file(self, tmp_path, capsys):
        command_file = tmp_path / "commands.txt"
        command_file.write_text("PLACE 0,0,NORTH\nREPORT\n")

        with patch("sys.argv", ["main", "-f", str(command_file)]):
            main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "0,0,NORTH"

    def test_multiple_reports(self, tmp_path, capsys):
        command_file = tmp_path / "commands.txt"
        command_file.write_text("PLACE 0,0,NORTH\nREPORT\nMOVE\nREPORT\n")

        with patch("sys.argv", ["main", "-f", str(command_file)]):
            main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "0,0,NORTH\n0,1,NORTH"

    def test_commands_before_place_ignored(self, tmp_path, capsys):
        command_file = tmp_path / "commands.txt"
        command_file.write_text("MOVE\nLEFT\nRIGHT\nREPORT\nPLACE 1,1,EAST\nREPORT\n")

        with patch("sys.argv", ["main", "-f", str(command_file)]):
            main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "1,1,EAST"

    def test_invalid_commands_skipped(self, tmp_path, capsys):
        command_file = tmp_path / "commands.txt"
        command_file.write_text("PLACE 0,0,NORTH\nFOO\nBAR\nREPORT\n")

        with patch("sys.argv", ["main", "-f", str(command_file)]):
            main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "0,0,NORTH"

    def test_nonexistent_file(self):
        with (
            patch("sys.argv", ["main", "-f", "nonexistent.txt"]),
            pytest.raises(FileNotFoundError),
        ):
            main()


class TestSubprocess:
    def test_file_mode_end_to_end(self, tmp_path):
        command_file = tmp_path / "commands.txt"
        command_file.write_text("PLACE 2,3,WEST\nMOVE\nREPORT\n")

        result = subprocess.run(
            [sys.executable, "main.py", "-f", str(command_file)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "1,3,WEST" in result.stdout

    def test_interactive_mode_end_to_end(self):
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="PLACE 0,0,NORTH\nMOVE\nREPORT\nEXIT\n",
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "0,1,NORTH" in result.stdout