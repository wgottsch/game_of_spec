"""Property-based tests for Conway's Game of Life rules.

Uses Hypothesis to verify that Conway's B3/S23 rules hold for
arbitrary grid configurations, ensuring correctness beyond
hand-crafted test patterns.
"""

from typing import FrozenSet, Tuple

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from game.core.grid import Grid

# ---------------------------------------------------------------------------
# Hypothesis strategies for generating valid game state
# ---------------------------------------------------------------------------

# Strategy for grid dimensions within valid range
grid_dimension = st.integers(min_value=10, max_value=30)


@st.composite
def valid_grid(draw: st.DrawFn) -> Grid:
    """Generate a random valid Grid with arbitrary live cells.

    Produces grids between 10x10 and 30x30 with a random subset
    of cells alive for property testing.
    """
    width = draw(grid_dimension)
    height = draw(grid_dimension)
    # Generate random live cell coordinates within bounds
    max_cells = min(width * height, 100)  # Cap for performance
    num_cells = draw(st.integers(min_value=0, max_value=max_cells))
    cells = draw(
        st.frozensets(
            st.tuples(
                st.integers(min_value=0, max_value=height - 1),
                st.integers(min_value=0, max_value=width - 1),
            ),
            min_size=0,
            max_size=num_cells,
        )
    )
    return Grid(width=width, height=height, live_cells=cells)


@st.composite
def grid_with_single_cell(draw: st.DrawFn) -> tuple:
    """Generate a grid with exactly one live cell and its coordinates."""
    width = draw(grid_dimension)
    height = draw(grid_dimension)
    row = draw(st.integers(min_value=0, max_value=height - 1))
    col = draw(st.integers(min_value=0, max_value=width - 1))
    grid = Grid(width=width, height=height, live_cells=frozenset({(row, col)}))
    return grid, row, col


# ---------------------------------------------------------------------------
# Conway's rule properties
# ---------------------------------------------------------------------------


class TestConwayRuleProperties:
    """Property-based tests for Conway's B3/S23 rules."""

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_grid_dimensions_preserved(self, grid: Grid) -> None:
        """Next generation must preserve grid width and height."""
        next_gen = grid.next_generation()
        assert next_gen.width == grid.width
        assert next_gen.height == grid.height

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_all_live_cells_within_bounds(self, grid: Grid) -> None:
        """All live cells in next generation must be within grid bounds."""
        next_gen = grid.next_generation()
        for row, col in next_gen.live_cells:
            assert (
                0 <= row < next_gen.height
            ), f"Row {row} out of bounds (height={next_gen.height})"
            assert (
                0 <= col < next_gen.width
            ), f"Col {col} out of bounds (width={next_gen.width})"

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_survival_rule_two_or_three_neighbors(self, grid: Grid) -> None:
        """A live cell with 2 or 3 neighbors must survive to next gen."""
        next_gen = grid.next_generation()
        for row, col in grid.live_cells:
            neighbors = grid.count_live_neighbors(row, col)
            if neighbors in (2, 3):
                assert (row, col) in next_gen.live_cells, (
                    f"Live cell ({row},{col}) with {neighbors} neighbors "
                    f"should survive but died"
                )

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_death_rule_underpopulation(self, grid: Grid) -> None:
        """A live cell with fewer than 2 neighbors must die."""
        next_gen = grid.next_generation()
        for row, col in grid.live_cells:
            neighbors = grid.count_live_neighbors(row, col)
            if neighbors < 2:
                assert (row, col) not in next_gen.live_cells, (
                    f"Live cell ({row},{col}) with {neighbors} neighbors "
                    f"should die from underpopulation but survived"
                )

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_death_rule_overpopulation(self, grid: Grid) -> None:
        """A live cell with more than 3 neighbors must die."""
        next_gen = grid.next_generation()
        for row, col in grid.live_cells:
            neighbors = grid.count_live_neighbors(row, col)
            if neighbors > 3:
                assert (row, col) not in next_gen.live_cells, (
                    f"Live cell ({row},{col}) with {neighbors} neighbors "
                    f"should die from overpopulation but survived"
                )

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_birth_rule_exactly_three_neighbors(self, grid: Grid) -> None:
        """A dead cell with exactly 3 neighbors must become alive."""
        next_gen = grid.next_generation()
        # Check all cells that are dead in current gen but have 3 neighbors
        for row in range(grid.height):
            for col in range(grid.width):
                if (row, col) not in grid.live_cells:
                    neighbors = grid.count_live_neighbors(row, col)
                    if neighbors == 3:
                        assert (row, col) in next_gen.live_cells, (
                            f"Dead cell ({row},{col}) with 3 neighbors "
                            f"should be born but remained dead"
                        )

    @given(grid=valid_grid())
    @settings(max_examples=100)
    def test_empty_grid_stays_empty(self, grid: Grid) -> None:
        """An empty grid must remain empty after any number of generations."""
        empty = Grid(width=grid.width, height=grid.height, live_cells=frozenset())
        next_gen = empty.next_generation()
        assert next_gen.population == 0

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_neighbor_count_range(self, grid: Grid) -> None:
        """Neighbor count must always be between 0 and 8."""
        for row in range(grid.height):
            for col in range(grid.width):
                count = grid.count_live_neighbors(row, col)
                assert (
                    0 <= count <= 8
                ), f"Neighbor count {count} at ({row},{col}) out of range"

    @given(data=grid_with_single_cell())
    @settings(max_examples=100)
    def test_isolated_cell_dies(self, data: tuple) -> None:
        """A single isolated cell with no neighbors must die."""
        grid, row, col = data
        # Ensure only one cell is alive
        assume(grid.population == 1)
        next_gen = grid.next_generation()
        assert (
            row,
            col,
        ) not in next_gen.live_cells, "Isolated cell should die from underpopulation"

    @given(grid=valid_grid())
    @settings(max_examples=200)
    def test_next_generation_is_immutable(self, grid: Grid) -> None:
        """Advancing a generation must not modify the original grid."""
        original_live = frozenset(grid.live_cells)
        original_population = grid.population
        _ = grid.next_generation()
        assert grid.live_cells == original_live
        assert grid.population == original_population
