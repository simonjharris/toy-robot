import pytest

from toy_robot.data_classes import Point
from toy_robot.table import Table


class TestTable:
    def test_table_init_rejects_negative_and_zero_width(self) -> None:
        with pytest.raises(ValueError):
            Table(width=0)

        with pytest.raises(ValueError):
            Table(width=-1)

    def test_table_init_rejects_negative_and_zero_height(self) -> None:
        with pytest.raises(ValueError):
            Table(height=0)

        with pytest.raises(ValueError):
            Table(height=-1)

    @pytest.mark.parametrize(
        ["coordinate", "is_valid"],
        [
            [Point(0, 0), True],  # origin
            [Point(2, 2), True],  # centre
            [Point(0, 5), False],  # out of bounds north
            [Point(5, 0), False],  # out of bounds east
            [Point(0, -1), False],  # out of bounds south
            [Point(-1, 0), False],  #  out of bounds west
        ],
    )
    def test_is_point_valid(
        self, five_unit_square_table: Table, coordinate: Point, is_valid: bool
    ) -> None:
        assert five_unit_square_table.is_valid_position(coordinate) == is_valid
