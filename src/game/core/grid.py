"""Grid management for Conway's Game of Life.

Implements the immutable Grid dataclass with set-based live cell tracking,
neighbor counting, Conway's rule application, and cell manipulation.
"""

from dataclasses import dataclass, field
from typing import FrozenSet, Iterator, List, Set, Tuple

from game.core.cell import Cell
from game.core.exceptions import CellCoordinateError, InvalidGridDimensionsError

# Pre-computed neighbor offsets for the 8 surrounding cells
_NEIGHBOR_OFFSETS: List[Tuple[int, int]] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


@dataclass(frozen=True)
class Grid:
    """Immutable grid representing the complete game state.

    Uses a set of (row, col) tuples to track live cells, providing O(1)
    lookup and efficient iteration over only the living population.
    Dead cells outside the live set are implicitly dead.

    Attributes:
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        live_cells: Frozenset of (row, col) coordinates for living cells.
    """

    width: int
    height: int
    live_cells: FrozenSet[Tuple[int, int]] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Validate grid dimensions after initialization.

        Raises:
            InvalidGridDimensionsError: If width or height is outside 10-200.
        """
        if not (10 <= self.width <= 200) or not (10 <= self.height <= 200):
            raise InvalidGridDimensionsError(self.width, self.height)

    def is_valid_coordinate(self, row: int, col: int) -> bool:
        """Check if coordinates are within grid bounds.

        Args:
            row: Row coordinate to validate.
            col: Column coordinate to validate.

        Returns:
            True if (row, col) is within the grid.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def is_alive(self, row: int, col: int) -> bool:
        """Check if a cell at the given coordinates is alive.

        Args:
            row: Cell row coordinate.
            col: Cell column coordinate.

        Returns:
            True if the cell is alive, False otherwise.
        """
        return (row, col) in self.live_cells

    def get_cell(self, row: int, col: int) -> Cell:
        """Get a Cell object at the specified coordinates.

        Args:
            row: Cell row coordinate.
            col: Cell column coordinate.

        Returns:
            Cell instance with the current state at (row, col).

        Raises:
            CellCoordinateError: If coordinates are outside grid bounds.
        """
        if not self.is_valid_coordinate(row, col):
            raise CellCoordinateError(row, col)
        return Cell(row=row, col=col, is_alive=(row, col) in self.live_cells)

    def set_cell(self, row: int, col: int, alive: bool) -> "Grid":
        """Return a new Grid with the specified cell state changed.

        Args:
            row: Target cell row coordinate.
            col: Target cell column coordinate.
            alive: Desired living state for the cell.

        Returns:
            New Grid instance with the cell state updated.

        Raises:
            CellCoordinateError: If coordinates are outside grid bounds.
        """
        if not self.is_valid_coordinate(row, col):
            raise CellCoordinateError(row, col)

        coord = (row, col)
        if alive:
            # Add cell to live set
            new_live = self.live_cells | frozenset({coord})
        else:
            # Remove cell from live set
            new_live = self.live_cells - frozenset({coord})

        return Grid(width=self.width, height=self.height, live_cells=new_live)

    def toggle_cell(self, row: int, col: int) -> "Grid":
        """Return a new Grid with the specified cell state toggled.

        Args:
            row: Target cell row coordinate.
            col: Target cell column coordinate.

        Returns:
            New Grid with the cell's alive state inverted.

        Raises:
            CellCoordinateError: If coordinates are outside grid bounds.
        """
        if not self.is_valid_coordinate(row, col):
            raise CellCoordinateError(row, col)

        coord = (row, col)
        currently_alive = coord in self.live_cells
        return self.set_cell(row, col, not currently_alive)

    def count_live_neighbors(self, row: int, col: int) -> int:
        """Count the number of living neighbors for a cell.

        Checks all 8 surrounding cells. Cells outside the grid boundary
        are treated as dead (finite grid with dead boundaries).

        Args:
            row: Cell row coordinate.
            col: Cell column coordinate.

        Returns:
            Number of living neighbors (0-8).
        """
        count = 0
        for dr, dc in _NEIGHBOR_OFFSETS:
            neighbor_row, neighbor_col = row + dr, col + dc
            # Boundary cells outside grid are implicitly dead
            if (neighbor_row, neighbor_col) in self.live_cells:
                count += 1
        return count

    def next_generation(self) -> "Grid":
        """Apply Conway's B3/S23 rules to produce the next generation.

        Rules:
        - A live cell with 2 or 3 neighbors survives.
        - A dead cell with exactly 3 neighbors becomes alive.
        - All other cells die or stay dead.

        Only inspects cells that are alive or adjacent to alive cells,
        avoiding full grid iteration for sparse populations.

        Returns:
            New Grid instance representing the next generation.
        """
        # Collect all candidate cells: live cells + their neighbors
        candidates: Set[Tuple[int, int]] = set()
        for row, col in self.live_cells:
            candidates.add((row, col))
            for dr, dc in _NEIGHBOR_OFFSETS:
                nr, nc = row + dr, col + dc
                # Only consider candidates within grid bounds
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    candidates.add((nr, nc))

        # Apply Conway's rules to each candidate
        new_live: Set[Tuple[int, int]] = set()
        for row, col in candidates:
            neighbor_count = self.count_live_neighbors(row, col)
            currently_alive = (row, col) in self.live_cells

            if currently_alive and neighbor_count in (2, 3):
                # Survival: live cell with 2 or 3 neighbors lives on
                new_live.add((row, col))
            elif not currently_alive and neighbor_count == 3:
                # Birth: dead cell with exactly 3 neighbors becomes alive
                new_live.add((row, col))
            # All other cases: cell dies or stays dead (not added)

        return Grid(
            width=self.width,
            height=self.height,
            live_cells=frozenset(new_live),
        )

    def clear(self) -> "Grid":
        """Return a new empty Grid with the same dimensions.

        Returns:
            New Grid with no living cells.
        """
        return Grid(width=self.width, height=self.height, live_cells=frozenset())

    @property
    def population(self) -> int:
        """Get the current number of living cells.

        Returns:
            Count of alive cells in the grid.
        """
        return len(self.live_cells)

    def iter_live_cells(self) -> Iterator[Tuple[int, int]]:
        """Iterate over all living cell coordinates.

        Yields:
            Tuples of (row, col) for each living cell.
        """
        yield from self.live_cells

    @staticmethod
    def create_empty(width: int, height: int) -> "Grid":
        """Factory method to create an empty grid.

        Args:
            width: Grid width in cells (10-200).
            height: Grid height in cells (10-200).

        Returns:
            New empty Grid instance.

        Raises:
            InvalidGridDimensionsError: If dimensions are invalid.
        """
        return Grid(width=width, height=height, live_cells=frozenset())
