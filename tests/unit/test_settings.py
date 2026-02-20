"""Unit tests for GameConfig validation.

Tests Pydantic model field constraints, computed properties,
and configuration immutability.
"""

import pytest

from game.config.settings import GameConfig


class TestGameConfigDefaults:
    """Tests for default configuration values."""

    def test_default_grid_dimensions(self) -> None:
        """Default grid is 50x50."""
        config = GameConfig()
        assert config.grid_width == 50
        assert config.grid_height == 50

    def test_default_cell_size(self) -> None:
        """Default cell size is 12 pixels."""
        config = GameConfig()
        assert config.cell_size == 12

    def test_default_speed(self) -> None:
        """Default speed level is 3."""
        config = GameConfig()
        assert config.default_speed == 3

    def test_default_fps(self) -> None:
        """Default target FPS is 60."""
        config = GameConfig()
        assert config.target_fps == 60

    def test_default_window_title(self) -> None:
        """Default window title is correct."""
        config = GameConfig()
        assert config.window_title == "Conway's Game of Life"


class TestGameConfigValidation:
    """Tests for field constraint validation."""

    def test_grid_width_minimum(self) -> None:
        """Grid width must be >= 10."""
        with pytest.raises(Exception):
            GameConfig(grid_width=9)

    def test_grid_width_maximum(self) -> None:
        """Grid width must be <= 200."""
        with pytest.raises(Exception):
            GameConfig(grid_width=201)

    def test_grid_height_minimum(self) -> None:
        """Grid height must be >= 10."""
        with pytest.raises(Exception):
            GameConfig(grid_height=9)

    def test_grid_height_maximum(self) -> None:
        """Grid height must be <= 200."""
        with pytest.raises(Exception):
            GameConfig(grid_height=201)

    def test_cell_size_minimum(self) -> None:
        """Cell size must be >= 3."""
        with pytest.raises(Exception):
            GameConfig(cell_size=2)

    def test_cell_size_maximum(self) -> None:
        """Cell size must be <= 50."""
        with pytest.raises(Exception):
            GameConfig(cell_size=51)

    def test_speed_minimum(self) -> None:
        """Default speed must be >= 1."""
        with pytest.raises(Exception):
            GameConfig(default_speed=0)

    def test_speed_maximum(self) -> None:
        """Default speed must be <= 10."""
        with pytest.raises(Exception):
            GameConfig(default_speed=11)

    def test_fps_minimum(self) -> None:
        """Target FPS must be >= 10."""
        with pytest.raises(Exception):
            GameConfig(target_fps=5)

    def test_fps_maximum(self) -> None:
        """Target FPS must be <= 120."""
        with pytest.raises(Exception):
            GameConfig(target_fps=121)

    def test_valid_boundary_values(self) -> None:
        """Boundary values at min and max are accepted."""
        config = GameConfig(
            grid_width=10,
            grid_height=10,
            cell_size=3,
            default_speed=1,
            target_fps=10,
        )
        assert config.grid_width == 10

    def test_delay_ordering_valid(self) -> None:
        """Config accepts max > min delay."""
        config = GameConfig(max_generation_delay_ms=500, min_generation_delay_ms=50)
        assert config.max_generation_delay_ms > config.min_generation_delay_ms

    def test_delay_ordering_invalid(self) -> None:
        """Config rejects max <= min delay."""
        with pytest.raises(Exception):
            GameConfig(max_generation_delay_ms=50, min_generation_delay_ms=100)


class TestGameConfigImmutability:
    """Tests for frozen Pydantic model."""

    def test_cannot_modify_grid_width(self) -> None:
        """Frozen config prevents width modification."""
        config = GameConfig()
        with pytest.raises(Exception):
            config.grid_width = 100  # type: ignore[misc]

    def test_cannot_modify_cell_size(self) -> None:
        """Frozen config prevents cell_size modification."""
        config = GameConfig()
        with pytest.raises(Exception):
            config.cell_size = 20  # type: ignore[misc]


class TestGameConfigComputedProperties:
    """Tests for calculated window dimensions and delays."""

    def test_window_width_calculation(self) -> None:
        """Window width = grid_width * cell_size."""
        config = GameConfig(grid_width=30, cell_size=15)
        assert config.calculate_window_width() == 450

    def test_window_height_includes_panel(self) -> None:
        """Window height = grid_height * cell_size + ui_panel_height."""
        config = GameConfig(grid_height=20, cell_size=10, ui_panel_height=60)
        assert config.calculate_window_height() == 260

    def test_delay_for_speed_1_is_max(self) -> None:
        """Speed level 1 returns maximum delay."""
        config = GameConfig(max_generation_delay_ms=1000, min_generation_delay_ms=50)
        assert config.calculate_delay_for_speed(1) == 1000

    def test_delay_for_speed_10_is_min(self) -> None:
        """Speed level 10 returns minimum delay."""
        config = GameConfig(max_generation_delay_ms=1000, min_generation_delay_ms=50)
        assert config.calculate_delay_for_speed(10) == 50

    def test_delay_decreases_with_speed(self) -> None:
        """Each speed level produces equal or smaller delay than the previous."""
        config = GameConfig()
        for speed in range(1, 10):
            assert config.calculate_delay_for_speed(
                speed
            ) >= config.calculate_delay_for_speed(speed + 1)
