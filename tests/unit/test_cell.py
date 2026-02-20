"""Unit tests for the Cell entity.

Tests Cell creation, immutability, coordinate access, and state transitions.
"""

import pytest

from game.core.cell import Cell


class TestCellCreation:
    """Tests for Cell initialization and default values."""

    def test_create_cell_with_defaults(self) -> None:
        """Cell created without is_alive defaults to dead."""
        cell = Cell(row=0, col=0)
        assert cell.row == 0
        assert cell.col == 0
        assert cell.is_alive is False

    def test_create_alive_cell(self) -> None:
        """Cell can be created with is_alive=True."""
        cell = Cell(row=3, col=7, is_alive=True)
        assert cell.row == 3
        assert cell.col == 7
        assert cell.is_alive is True

    def test_create_dead_cell_explicitly(self) -> None:
        """Cell can be explicitly created as dead."""
        cell = Cell(row=1, col=2, is_alive=False)
        assert cell.is_alive is False

    def test_negative_coordinates_allowed(self) -> None:
        """Cell allows negative coordinates (validation is Grid's job)."""
        cell = Cell(row=-1, col=-5)
        assert cell.row == -1
        assert cell.col == -5


class TestCellImmutability:
    """Tests for Cell frozen dataclass immutability."""

    def test_cannot_modify_row(self) -> None:
        """Attempting to change row raises FrozenInstanceError."""
        cell = Cell(row=0, col=0)
        with pytest.raises(AttributeError):
            cell.row = 5  # type: ignore[misc]

    def test_cannot_modify_col(self) -> None:
        """Attempting to change col raises FrozenInstanceError."""
        cell = Cell(row=0, col=0)
        with pytest.raises(AttributeError):
            cell.col = 5  # type: ignore[misc]

    def test_cannot_modify_is_alive(self) -> None:
        """Attempting to change is_alive raises FrozenInstanceError."""
        cell = Cell(row=0, col=0, is_alive=True)
        with pytest.raises(AttributeError):
            cell.is_alive = False  # type: ignore[misc]


class TestCellCoordinate:
    """Tests for Cell.coordinate() method."""

    def test_coordinate_returns_tuple(self) -> None:
        """coordinate() returns a (row, col) tuple."""
        cell = Cell(row=4, col=8)
        assert cell.coordinate() == (4, 8)

    def test_coordinate_origin(self) -> None:
        """coordinate() works for origin cell."""
        cell = Cell(row=0, col=0)
        assert cell.coordinate() == (0, 0)


class TestCellWithState:
    """Tests for Cell.with_state() method."""

    def test_with_state_alive(self) -> None:
        """with_state(True) creates alive cell at same position."""
        cell = Cell(row=3, col=5, is_alive=False)
        new_cell = cell.with_state(True)
        assert new_cell.row == 3
        assert new_cell.col == 5
        assert new_cell.is_alive is True

    def test_with_state_dead(self) -> None:
        """with_state(False) creates dead cell at same position."""
        cell = Cell(row=3, col=5, is_alive=True)
        new_cell = cell.with_state(False)
        assert new_cell.is_alive is False

    def test_with_state_returns_new_instance(self) -> None:
        """with_state() returns a new Cell, not the original."""
        cell = Cell(row=1, col=1, is_alive=True)
        new_cell = cell.with_state(True)
        assert cell is not new_cell

    def test_with_state_preserves_coordinates(self) -> None:
        """with_state() preserves original row and col values."""
        cell = Cell(row=7, col=9, is_alive=False)
        new_cell = cell.with_state(True)
        assert new_cell.coordinate() == cell.coordinate()


class TestCellEquality:
    """Tests for Cell equality comparison (dataclass __eq__)."""

    def test_equal_cells(self) -> None:
        """Two cells with same attributes are equal."""
        cell_a = Cell(row=1, col=2, is_alive=True)
        cell_b = Cell(row=1, col=2, is_alive=True)
        assert cell_a == cell_b

    def test_different_state_not_equal(self) -> None:
        """Cells at same position with different states are not equal."""
        cell_a = Cell(row=1, col=2, is_alive=True)
        cell_b = Cell(row=1, col=2, is_alive=False)
        assert cell_a != cell_b

    def test_different_position_not_equal(self) -> None:
        """Cells at different positions are not equal."""
        cell_a = Cell(row=1, col=2)
        cell_b = Cell(row=3, col=4)
        assert cell_a != cell_b

    def test_cell_is_hashable(self) -> None:
        """Frozen cells can be used in sets and as dict keys."""
        cell = Cell(row=1, col=2, is_alive=True)
        cell_set = {cell}
        assert cell in cell_set
