import argparse
import sys
import textwrap
from importlib.metadata import PackageNotFoundError, version

from src.robot import Robot
from src.simulator import RobotSimulator, Signal
from src.table import Table


def _get_version() -> str:
    try:
        return version("toy-robot")
    except PackageNotFoundError:
        return "dev"


def main():
    app_version = _get_version()
    arg_parser = argparse.ArgumentParser(
        description=f"Toy Robot Simulator v{app_version}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Available commands:
              PLACE <x>,<y>,<DIRECTION>  e.g. PLACE 0,0,NORTH : Place the robot at the specified position.
              LEFT                       : Turn the robot 90 degrees to the left.
              RIGHT                      : Turn the robot 90 degrees to the right.
              MOVE                       : Move the robot forward one place in the current direction of the robot.
              REPORT                     : Display the current state of the robot, i.e. its current x,y position and direction.
              EXIT                       : Exit the simulator
            """,
        ),
    )
    arg_parser.add_argument("-f", "--file", help="path to file containing commands")

    simulator = RobotSimulator(robot=Robot(), table=Table())

    args = arg_parser.parse_args()
    if args.file:
        with open(args.file, "r") as command_file:
            if output := simulator.process_commands(command_file):
                print(output)

    else:
        print(
            f"Welcome to the Robot Simulator v{app_version}\n\n"
            "All commands should be in uppercase\n"
            "Type EXIT or ctrl+c when you are done\n"
            "Full command list can be seen by exiting and running this tool with the --help flag\n"
            "Enter a PLACE command to start:"
        )
        while True:
            try:
                user_command = input("> ")
                output = simulator.process_command(user_command)
                if output == Signal.EXIT:
                    sys.exit(0)
                if output:
                    print(output)

            except KeyboardInterrupt:
                # exit gracefully if using ctrl+c
                sys.exit(0)


if __name__ == "__main__":
    main()
