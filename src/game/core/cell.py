"""Cell entity for Conway's Game of Life.

Defines the immutable Cell dataclass representing a single grid unit
with coordinates and binary alive/dead state.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Cell:
    """Immutable cell with grid coordinates and living state.

    Represents a single unit in the Game of Life grid. Frozen to enforce
    immutability — state changes produce new Cell instances.

    Attributes:
        row: Zero-based row position in the grid.
        col: Zero-based column position in the grid.
        is_alive: Whether the cell is currently alive.
    """

    row: int
    col: int
    is_alive: bool = False

    def coordinate(self) -> Tuple[int, int]:
        """Get cell position as a (row, col) tuple.

        Returns:
            Tuple of (row, col) coordinates.
        """
        return (self.row, self.col)

    def with_state(self, alive: bool) -> "Cell":
        """Create a new Cell with a different living state.

        Args:
            alive: The new living state for the cell.

        Returns:
            New Cell instance at the same position with updated state.
        """
        return Cell(row=self.row, col=self.col, is_alive=alive)
