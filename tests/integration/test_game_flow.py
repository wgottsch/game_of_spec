"""Integration tests for the complete game flow.

Tests end-to-end scenarios including simulation lifecycle,
pattern evolution, and state management across components.
"""

from typing import FrozenSet, Tuple

import pytest

from game.config.settings import GameConfig
from game.core.grid import Grid
from game.core.simulation import SimulationController, SimulationMode


class TestGameFlowSimulationLifecycle:
    """Tests for complete simulation lifecycle scenarios."""

    def test_create_start_advance_pause(self) -> None:
        """Full lifecycle: create grid → start → advance → pause."""
        config = GameConfig(grid_width=10, grid_height=10)
        # Horizontal blinker
        live: FrozenSet[Tuple[int, int]] = frozenset({(5, 4), (5, 5), (5, 6)})
        grid = Grid(width=10, height=10, live_cells=live)
        controller = SimulationController(config=config, grid=grid)

        # Start simulation
        controller.start()
        assert controller.state.mode == SimulationMode.RUNNING

        # Advance one generation
        controller.advance()
        assert controller.state.generation == 1
        # Blinker should have rotated to vertical
        new_grid = controller.state.current_grid
        assert new_grid.is_alive(4, 5)
        assert new_grid.is_alive(5, 5)
        assert new_grid.is_alive(6, 5)

        # Pause
        controller.pause()
        assert controller.state.mode == SimulationMode.PAUSED
        # Grid state preserved during pause
        assert controller.state.current_grid.population == 3

    def test_toggle_cell_while_paused(self) -> None:
        """Cell can be toggled while simulation is paused."""
        config = GameConfig(grid_width=10, grid_height=10)
        grid = Grid.create_empty(10, 10)
        controller = SimulationController(config=config, grid=grid)

        # Toggle a cell
        new_grid = controller.state.current_grid.toggle_cell(5, 5)
        controller.update_grid(new_grid)
        assert controller.state.current_grid.is_alive(5, 5)

        # Toggle it back
        new_grid = controller.state.current_grid.toggle_cell(5, 5)
        controller.update_grid(new_grid)
        assert not controller.state.current_grid.is_alive(5, 5)

    def test_clear_resets_everything(self) -> None:
        """Clear grid resets generation and stops simulation."""
        config = GameConfig(grid_width=10, grid_height=10)
        live: FrozenSet[Tuple[int, int]] = frozenset({(5, 4), (5, 5), (5, 6)})
        grid = Grid(width=10, height=10, live_cells=live)
        controller = SimulationController(config=config, grid=grid)

        controller.start()
        controller.advance()
        controller.advance()
        assert controller.state.generation == 2

        # Clear
        empty_grid = controller.state.current_grid.clear()
        controller.reset(empty_grid)

        assert controller.state.generation == 0
        assert controller.state.mode == SimulationMode.STOPPED
        assert controller.state.current_grid.population == 0

    def test_speed_changes_during_simulation(self) -> None:
        """Speed can be adjusted while simulation runs."""
        config = GameConfig(grid_width=10, grid_height=10)
        grid = Grid.create_empty(10, 10)
        controller = SimulationController(config=config, grid=grid)

        initial_speed = controller.state.speed_level
        controller.start()
        controller.increase_speed()
        controller.increase_speed()
        assert controller.state.speed_level == initial_speed + 2
        assert controller.state.mode == SimulationMode.RUNNING

    def test_multiple_generation_blinker_cycle(self) -> None:
        """Blinker returns to original state after 2 generations."""
        config = GameConfig(grid_width=10, grid_height=10)
        live: FrozenSet[Tuple[int, int]] = frozenset({(4, 5), (5, 5), (6, 5)})
        grid = Grid(width=10, height=10, live_cells=live)
        controller = SimulationController(config=config, grid=grid)

        original_cells = controller.state.current_grid.live_cells
        controller.start()
        controller.advance()  # Gen 1: horizontal
        controller.advance()  # Gen 2: vertical (original)

        assert controller.state.current_grid.live_cells == original_cells
        assert controller.state.generation == 2

    def test_glider_moves_over_generations(self) -> None:
        """Glider translates after 4 generations."""
        config = GameConfig(grid_width=20, grid_height=20)
        live: FrozenSet[Tuple[int, int]] = frozenset(
            {
                (1, 2),
                (2, 3),
                (3, 1),
                (3, 2),
                (3, 3),
            }
        )
        grid = Grid(width=20, height=20, live_cells=live)
        controller = SimulationController(config=config, grid=grid)

        controller.start()
        for _ in range(4):
            controller.advance()

        # After 4 gens, glider has 5 cells and moved diagonally
        assert controller.state.current_grid.population == 5
        assert controller.state.generation == 4


class TestStartupConfigurationFlow:
    """Tests for grid configuration at startup."""

    def test_custom_grid_dimensions(self) -> None:
        """Application accepts custom grid dimensions."""
        config = GameConfig(grid_width=30, grid_height=25, cell_size=15)
        grid = Grid.create_empty(config.grid_width, config.grid_height)
        assert grid.width == 30
        assert grid.height == 25

    def test_maximum_grid_dimensions(self) -> None:
        """Application handles maximum 200x200 grid."""
        config = GameConfig(grid_width=200, grid_height=200, cell_size=3)
        grid = Grid.create_empty(config.grid_width, config.grid_height)
        assert grid.population == 0

    def test_minimum_grid_dimensions(self) -> None:
        """Application handles minimum 10x10 grid."""
        config = GameConfig(grid_width=10, grid_height=10, cell_size=50)
        grid = Grid.create_empty(config.grid_width, config.grid_height)
        assert grid.width == 10

    def test_window_size_matches_config(self) -> None:
        """Window dimensions calculate correctly from config."""
        config = GameConfig(grid_width=40, grid_height=30, cell_size=10)
        assert config.calculate_window_width() == 400
        expected_height = 300 + config.ui_panel_height
        assert config.calculate_window_height() == expected_height
