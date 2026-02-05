from robot import Robot
from table import Table


class RobotSimulator:
    def __init__(self, robot: Robot, table: Table):
        self.robot = robot
        self.table = table
