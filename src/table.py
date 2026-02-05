from data_classes import Point
from robot import Robot


class Table:
    """A rectangular table surface for a robot to move on.

    The table uses a coordinate system where Point(0, 0) is the south-west corner.
    Therefore, both values must be positive integers.
    """

    def __init__(
        self,
        width: int = 5,
        height: int = 5,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")

        self.width = width
        self.height = height

    def is_valid_point(self, point: Point) -> bool:
        """Check if a point is valid. I.e. not outside the bounds of the table.

        Args:
            point (Point): The point to be checked.

        Returns:
            bool: True if the point is valid, False otherwise.
        """
        return 0 <= point.x < self.width and 0 <= point.y < self.height
