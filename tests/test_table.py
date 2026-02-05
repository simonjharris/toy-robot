import pytest

from data_classes import Point
from table import Table


class TestTable:
    @pytest.mark.parametrize(
        ["coordinate", "is_valid"],
        [
            [Point(0, 0), True],  # origin
            [Point(2, 2), True],  # centre
            [Point(0, 5), False],  # too far north
            [Point(5, 0), False],  # too far east
            [Point(0, -1), False],  # too far south
            [Point(-1, 0), False],  #  too far west
        ],
    )
    def test_is_point_valid(
        self, five_unit_square_table: Table, coordinate: Point, is_valid: bool
    ) -> None:
        assert five_unit_square_table.is_valid_point(coordinate) == is_valid
