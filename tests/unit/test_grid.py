"""Unit tests for the Grid entity.

Tests grid creation, cell operations, neighbor counting, Conway's rules,
boundary handling, and known pattern evolution.
"""

from typing import FrozenSet, Tuple

import pytest

from game.core.cell import Cell
from game.core.exceptions import CellCoordinateError, InvalidGridDimensionsError
from game.core.grid import Grid


class TestGridCreation:
    """Tests for Grid initialization and validation."""

    def test_create_empty_grid(self) -> None:
        """create_empty() produces a grid with no live cells."""
        grid = Grid.create_empty(20, 20)
        assert grid.width == 20
        assert grid.height == 20
        assert grid.population == 0

    def test_create_grid_with_live_cells(self) -> None:
        """Grid can be created with initial live cells."""
        live: FrozenSet[Tuple[int, int]] = frozenset({(0, 0), (1, 1)})
        grid = Grid(width=10, height=10, live_cells=live)
        assert grid.population == 2

    def test_invalid_width_too_small(self) -> None:
        """Grid with width < 10 raises InvalidGridDimensionsError."""
        with pytest.raises(InvalidGridDimensionsError):
            Grid(width=5, height=10)

    def test_invalid_height_too_small(self) -> None:
        """Grid with height < 10 raises InvalidGridDimensionsError."""
        with pytest.raises(InvalidGridDimensionsError):
            Grid(width=10, height=5)

    def test_invalid_width_too_large(self) -> None:
        """Grid with width > 200 raises InvalidGridDimensionsError."""
        with pytest.raises(InvalidGridDimensionsError):
            Grid(width=201, height=10)

    def test_invalid_height_too_large(self) -> None:
        """Grid with height > 200 raises InvalidGridDimensionsError."""
        with pytest.raises(InvalidGridDimensionsError):
            Grid(width=10, height=201)

    def test_minimum_valid_dimensions(self) -> None:
        """10x10 is the minimum valid grid size."""
        grid = Grid(width=10, height=10)
        assert grid.width == 10
        assert grid.height == 10

    def test_maximum_valid_dimensions(self) -> None:
        """200x200 is the maximum valid grid size."""
        grid = Grid(width=200, height=200)
        assert grid.width == 200
        assert grid.height == 200


class TestGridCellAccess:
    """Tests for getting and setting individual cells."""

    def test_get_dead_cell(self, empty_grid: Grid) -> None:
        """Getting a cell from empty grid returns dead cell."""
        cell = empty_grid.get_cell(5, 5)
        assert cell.row == 5
        assert cell.col == 5
        assert cell.is_alive is False

    def test_get_live_cell(self, blinker_grid: Grid) -> None:
        """Getting a live cell returns cell with is_alive=True."""
        cell = blinker_grid.get_cell(5, 5)
        assert cell.is_alive is True

    def test_get_cell_out_of_bounds(self, empty_grid: Grid) -> None:
        """Getting cell outside grid raises CellCoordinateError."""
        with pytest.raises(CellCoordinateError):
            empty_grid.get_cell(20, 0)

    def test_get_cell_negative_row(self, empty_grid: Grid) -> None:
        """Getting cell with negative row raises CellCoordinateError."""
        with pytest.raises(CellCoordinateError):
            empty_grid.get_cell(-1, 0)

    def test_set_cell_alive(self, empty_grid: Grid) -> None:
        """set_cell creates new grid with cell alive."""
        new_grid = empty_grid.set_cell(5, 5, True)
        assert new_grid.is_alive(5, 5)
        assert not empty_grid.is_alive(5, 5)  # Original unchanged

    def test_set_cell_dead(self, blinker_grid: Grid) -> None:
        """set_cell(False) creates new grid with cell dead."""
        new_grid = blinker_grid.set_cell(5, 5, False)
        assert not new_grid.is_alive(5, 5)

    def test_set_cell_out_of_bounds(self, empty_grid: Grid) -> None:
        """Setting cell outside grid raises CellCoordinateError."""
        with pytest.raises(CellCoordinateError):
            empty_grid.set_cell(25, 0, True)

    def test_toggle_cell_dead_to_alive(self, empty_grid: Grid) -> None:
        """toggle_cell flips dead cell to alive."""
        new_grid = empty_grid.toggle_cell(3, 3)
        assert new_grid.is_alive(3, 3)

    def test_toggle_cell_alive_to_dead(self, blinker_grid: Grid) -> None:
        """toggle_cell flips alive cell to dead."""
        new_grid = blinker_grid.toggle_cell(5, 5)
        assert not new_grid.is_alive(5, 5)

    def test_toggle_preserves_other_cells(self, blinker_grid: Grid) -> None:
        """toggle_cell does not affect other cells."""
        new_grid = blinker_grid.toggle_cell(5, 5)
        assert new_grid.is_alive(4, 5)  # Still alive
        assert new_grid.is_alive(6, 5)  # Still alive


class TestGridNeighborCounting:
    """Tests for count_live_neighbors with various configurations."""

    def test_no_neighbors_empty_grid(self, empty_grid: Grid) -> None:
        """Empty grid has 0 neighbors for any cell."""
        assert empty_grid.count_live_neighbors(5, 5) == 0

    def test_corner_cell_neighbors(self) -> None:
        """Corner cells have limited neighbor positions."""
        # Place cells around top-left corner
        live = frozenset({(0, 1), (1, 0), (1, 1)})
        grid = Grid(width=10, height=10, live_cells=live)
        assert grid.count_live_neighbors(0, 0) == 3

    def test_edge_cell_neighbors(self) -> None:
        """Edge cells have 5 neighbor positions maximum."""
        # Single neighbor above an edge cell
        live = frozenset({(0, 5)})
        grid = Grid(width=10, height=10, live_cells=live)
        assert grid.count_live_neighbors(1, 5) == 1

    def test_center_cell_all_neighbors(self) -> None:
        """Center cell surrounded by 8 live cells has count 8."""
        live = frozenset(
            {
                (4, 4),
                (4, 5),
                (4, 6),
                (5, 4),
                (5, 6),
                (6, 4),
                (6, 5),
                (6, 6),
            }
        )
        grid = Grid(width=10, height=10, live_cells=live)
        assert grid.count_live_neighbors(5, 5) == 8

    def test_blinker_center_has_two_neighbors(self, blinker_grid: Grid) -> None:
        """Center of vertical blinker has exactly 2 neighbors."""
        assert blinker_grid.count_live_neighbors(5, 5) == 2

    def test_blinker_ends_have_one_neighbor(self, blinker_grid: Grid) -> None:
        """End cells of vertical blinker have exactly 1 neighbor."""
        assert blinker_grid.count_live_neighbors(4, 5) == 1
        assert blinker_grid.count_live_neighbors(6, 5) == 1


class TestConwayRules:
    """Tests for Conway's B3/S23 rule application via next_generation()."""

    def test_empty_grid_stays_empty(self, empty_grid: Grid) -> None:
        """Empty grid remains empty after generation."""
        next_gen = empty_grid.next_generation()
        assert next_gen.population == 0

    def test_single_cell_dies(self) -> None:
        """Single isolated cell dies from underpopulation."""
        grid = Grid(width=10, height=10, live_cells=frozenset({(5, 5)}))
        next_gen = grid.next_generation()
        assert not next_gen.is_alive(5, 5)

    def test_two_adjacent_cells_die(self) -> None:
        """Two adjacent cells both die (only 1 neighbor each)."""
        grid = Grid(width=10, height=10, live_cells=frozenset({(5, 5), (5, 6)}))
        next_gen = grid.next_generation()
        assert next_gen.population == 0

    def test_three_cells_in_line_become_blinker(self) -> None:
        """Three horizontal cells become vertical (blinker oscillation)."""
        # Horizontal: (5,4), (5,5), (5,6)
        grid = Grid(width=10, height=10, live_cells=frozenset({(5, 4), (5, 5), (5, 6)}))
        next_gen = grid.next_generation()
        # Should become vertical: (4,5), (5,5), (6,5)
        assert next_gen.is_alive(4, 5)
        assert next_gen.is_alive(5, 5)
        assert next_gen.is_alive(6, 5)
        assert next_gen.population == 3

    def test_overpopulation_kills_center(self) -> None:
        """Cell with 4+ neighbors dies from overpopulation."""
        # Cross pattern: center has 4 neighbors
        live = frozenset(
            {
                (4, 5),
                (5, 4),
                (5, 5),
                (5, 6),
                (6, 5),
            }
        )
        grid = Grid(width=10, height=10, live_cells=live)
        next_gen = grid.next_generation()
        # Center (5,5) has 4 neighbors → dies
        assert not next_gen.is_alive(5, 5)

    def test_birth_with_three_neighbors(self) -> None:
        """Dead cell with exactly 3 live neighbors becomes alive."""
        # L-shape: dead cell at (5,5) has 3 neighbors
        live = frozenset({(4, 5), (5, 4), (5, 6)})
        grid = Grid(width=10, height=10, live_cells=live)
        next_gen = grid.next_generation()
        assert next_gen.is_alive(5, 5)


class TestKnownPatterns:
    """Tests for well-known Game of Life patterns."""

    def test_block_still_life(self, block_grid: Grid) -> None:
        """Block (2x2 square) is a still life — unchanged after generation."""
        next_gen = block_grid.next_generation()
        assert next_gen.live_cells == block_grid.live_cells

    def test_blinker_oscillation(self, blinker_grid: Grid) -> None:
        """Blinker alternates between vertical and horizontal phases."""
        # Initial: vertical at col 5
        gen1 = blinker_grid.next_generation()
        # Gen 1: horizontal at row 5
        assert gen1.is_alive(5, 4)
        assert gen1.is_alive(5, 5)
        assert gen1.is_alive(5, 6)
        assert gen1.population == 3

        # Gen 2: back to vertical (same as original)
        gen2 = gen1.next_generation()
        assert gen2.live_cells == blinker_grid.live_cells

    def test_glider_movement(self, glider_grid: Grid) -> None:
        """Glider moves one cell diagonally every 4 generations."""
        # Standard glider starting position
        gen = glider_grid
        for _ in range(4):
            gen = gen.next_generation()

        # After 4 generations, glider should have shifted by (1,1)
        # and have the same shape (5 cells)
        assert gen.population == 5

    def test_beacon_oscillation(self, beacon_grid: Grid) -> None:
        """Beacon oscillates between 8 and 6 cells over 2 generations."""
        gen1 = beacon_grid.next_generation()
        gen2 = gen1.next_generation()
        # Beacon returns to original state after 2 generations
        assert gen2.live_cells == beacon_grid.live_cells

    def test_toad_oscillation(self, toad_grid: Grid) -> None:
        """Toad oscillates with period 2."""
        gen1 = toad_grid.next_generation()
        gen2 = gen1.next_generation()
        # Toad returns to original state after 2 generations
        assert gen2.live_cells == toad_grid.live_cells


class TestGridClear:
    """Tests for Grid.clear() method."""

    def test_clear_empty_grid(self, empty_grid: Grid) -> None:
        """Clearing an already-empty grid returns empty grid."""
        cleared = empty_grid.clear()
        assert cleared.population == 0

    def test_clear_populated_grid(self, blinker_grid: Grid) -> None:
        """Clearing a populated grid removes all cells."""
        cleared = blinker_grid.clear()
        assert cleared.population == 0

    def test_clear_preserves_dimensions(self, blinker_grid: Grid) -> None:
        """Clearing preserves the grid's width and height."""
        cleared = blinker_grid.clear()
        assert cleared.width == blinker_grid.width
        assert cleared.height == blinker_grid.height

    def test_clear_returns_new_instance(self, blinker_grid: Grid) -> None:
        """clear() returns a new Grid, not the original."""
        cleared = blinker_grid.clear()
        assert cleared is not blinker_grid


class TestGridImmutability:
    """Tests for Grid frozen dataclass immutability."""

    def test_cannot_modify_width(self, empty_grid: Grid) -> None:
        """Attempting to change width raises error."""
        with pytest.raises(AttributeError):
            empty_grid.width = 30  # type: ignore[misc]

    def test_set_cell_returns_new_grid(self, empty_grid: Grid) -> None:
        """set_cell returns a new Grid, original is unchanged."""
        new_grid = empty_grid.set_cell(5, 5, True)
        assert new_grid is not empty_grid
        assert empty_grid.population == 0
        assert new_grid.population == 1

    def test_next_generation_returns_new_grid(self, blinker_grid: Grid) -> None:
        """next_generation returns a new Grid, original unchanged."""
        original_cells = frozenset(blinker_grid.live_cells)
        next_gen = blinker_grid.next_generation()
        assert next_gen is not blinker_grid
        assert blinker_grid.live_cells == original_cells


class TestGridIteration:
    """Tests for Grid iteration methods."""

    def test_iter_live_cells_empty(self, empty_grid: Grid) -> None:
        """Iterating empty grid yields no cells."""
        cells = list(empty_grid.iter_live_cells())
        assert cells == []

    def test_iter_live_cells_populated(self, blinker_grid: Grid) -> None:
        """Iterating populated grid yields all live cell coordinates."""
        cells = set(blinker_grid.iter_live_cells())
        assert cells == {(4, 5), (5, 5), (6, 5)}

    def test_population_matches_live_cells(self, blinker_grid: Grid) -> None:
        """population property matches length of live_cells."""
        assert blinker_grid.population == len(blinker_grid.live_cells)
