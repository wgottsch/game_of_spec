"""Unit tests for color constants.

Verifies that all color values are valid RGB tuples.
"""

from game.display import colors


class TestColorConstants:
    """Tests for all color constant definitions."""

    def _assert_valid_rgb(self, color: tuple, name: str) -> None:
        """Assert that a color is a valid RGB tuple with values 0-255."""
        assert isinstance(color, tuple), f"{name} is not a tuple"
        assert len(color) == 3, f"{name} does not have 3 components"
        for i, component in enumerate(color):
            assert 0 <= component <= 255, (
                f"{name}[{i}] = {component} is out of range 0-255"
            )

    def test_background_color(self) -> None:
        """Background is a valid RGB color."""
        self._assert_valid_rgb(colors.BACKGROUND, "BACKGROUND")

    def test_cell_alive_color(self) -> None:
        """CELL_ALIVE is a valid RGB color."""
        self._assert_valid_rgb(colors.CELL_ALIVE, "CELL_ALIVE")

    def test_cell_dead_color(self) -> None:
        """CELL_DEAD is a valid RGB color."""
        self._assert_valid_rgb(colors.CELL_DEAD, "CELL_DEAD")

    def test_grid_line_color(self) -> None:
        """GRID_LINE is a valid RGB color."""
        self._assert_valid_rgb(colors.GRID_LINE, "GRID_LINE")

    def test_ui_panel_colors(self) -> None:
        """All UI panel colors are valid RGB tuples."""
        self._assert_valid_rgb(colors.UI_PANEL_BG, "UI_PANEL_BG")
        self._assert_valid_rgb(colors.UI_PANEL_BORDER, "UI_PANEL_BORDER")
        self._assert_valid_rgb(colors.BUTTON_NORMAL, "BUTTON_NORMAL")
        self._assert_valid_rgb(colors.BUTTON_HOVER, "BUTTON_HOVER")
        self._assert_valid_rgb(colors.BUTTON_TEXT, "BUTTON_TEXT")

    def test_status_text_colors(self) -> None:
        """All status text colors are valid RGB tuples."""
        self._assert_valid_rgb(colors.STATUS_TEXT, "STATUS_TEXT")
        self._assert_valid_rgb(colors.GENERATION_TEXT, "GENERATION_TEXT")
        self._assert_valid_rgb(colors.SPEED_TEXT, "SPEED_TEXT")

    def test_mode_indicator_colors(self) -> None:
        """All mode indicator colors are valid RGB tuples."""
        self._assert_valid_rgb(colors.MODE_RUNNING, "MODE_RUNNING")
        self._assert_valid_rgb(colors.MODE_PAUSED, "MODE_PAUSED")
        self._assert_valid_rgb(colors.MODE_STOPPED, "MODE_STOPPED")

    def test_alive_visually_distinct_from_dead(self) -> None:
        """Alive and dead cell colors must be visually distinguishable."""
        assert colors.CELL_ALIVE != colors.CELL_DEAD
