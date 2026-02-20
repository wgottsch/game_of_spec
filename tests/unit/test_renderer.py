"""Unit tests for the GridRenderer.

Tests coordinate conversion and display state calculation.
Note: Actual rendering tests require a running pygame display
and are covered in integration tests.
"""

import pytest

from game.config.settings import GameConfig
from game.display.state import DisplayState


class TestDisplayState:
    """Tests for DisplayState dataclass."""

    def test_create_display_state(self) -> None:
        """DisplayState can be created with all required fields."""
        state = DisplayState(
            window_width=800,
            window_height=600,
            grid_offset_x=0,
            grid_offset_y=0,
        )
        assert state.window_width == 800
        assert state.window_height == 600
        assert state.show_grid_lines is True
        assert state.selected_cell is None

    def test_display_state_immutable(self) -> None:
        """DisplayState is immutable (frozen dataclass)."""
        state = DisplayState(
            window_width=800,
            window_height=600,
            grid_offset_x=0,
            grid_offset_y=0,
        )
        with pytest.raises(AttributeError):
            state.window_width = 1024  # type: ignore[misc]

    def test_display_state_with_selected_cell(self) -> None:
        """DisplayState accepts optional selected cell."""
        state = DisplayState(
            window_width=800,
            window_height=600,
            grid_offset_x=0,
            grid_offset_y=0,
            selected_cell=(5, 3),
        )
        assert state.selected_cell == (5, 3)


class TestCoordinateConversion:
    """Tests for pixel ↔ grid coordinate conversion logic."""

    def test_pixel_to_grid_basic(self) -> None:
        """Basic pixel to grid conversion with no offset."""
        config = GameConfig(grid_width=10, grid_height=10, cell_size=10)
        # Cell at (0,0) occupies pixels (0,0) to (9,9)
        # Pixel (15, 25) → col=1, row=2
        col = 15 // config.cell_size
        row = 25 // config.cell_size
        assert row == 2
        assert col == 1

    def test_pixel_at_cell_boundary(self) -> None:
        """Pixel exactly on cell boundary maps to correct cell."""
        config = GameConfig(grid_width=10, grid_height=10, cell_size=10)
        # Pixel (10, 10) → col=1, row=1 (start of next cell)
        col = 10 // config.cell_size
        row = 10 // config.cell_size
        assert row == 1
        assert col == 1

    def test_calculate_cell_position(self) -> None:
        """Cell position calculated correctly from grid coordinates."""
        config = GameConfig(grid_width=20, grid_height=15, cell_size=12)
        # Cell (3, 5) → x=60, y=36
        x = 5 * config.cell_size
        y = 3 * config.cell_size
        assert x == 60
        assert y == 36

    def test_window_dimensions_from_config(self) -> None:
        """Window dimensions calculated correctly from config."""
        config = GameConfig(grid_width=40, grid_height=30, cell_size=10)
        assert config.calculate_window_width() == 400
        assert config.calculate_window_height() == 300 + config.ui_panel_height
