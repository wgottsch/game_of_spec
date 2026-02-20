"""Display state model for rendering configuration.

Contains the DisplayState dataclass that tracks window dimensions,
grid offsets, and visual rendering options.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class DisplayState:
    """Immutable display configuration and rendering state.

    Tracks window dimensions, grid positioning, and visual options
    needed by the renderer to draw the game correctly.

    Attributes:
        window_width: Total window width in pixels.
        window_height: Total window height in pixels.
        grid_offset_x: Horizontal offset for grid centering in pixels.
        grid_offset_y: Vertical offset for grid centering in pixels.
        show_grid_lines: Whether grid boundary lines are visible.
        selected_cell: Currently highlighted cell coordinates, if any.
    """

    window_width: int
    window_height: int
    grid_offset_x: int
    grid_offset_y: int
    show_grid_lines: bool = True
    selected_cell: Optional[Tuple[int, int]] = None
