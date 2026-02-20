"""Unit tests for SimulationController and SimulationState.

Tests simulation mode transitions, speed control, timing logic,
and generation advancement.
"""

import time
from typing import FrozenSet, Tuple

import pytest

from game.config.settings import GameConfig
from game.core.exceptions import InvalidSpeedLevelError
from game.core.grid import Grid
from game.core.simulation import SimulationController, SimulationMode, SimulationState


class TestSimulationStateCreation:
    """Tests for SimulationState initialization."""

    def test_default_state(self, small_empty_grid: Grid) -> None:
        """Default SimulationState has generation 0, STOPPED, speed 3."""
        state = SimulationState(current_grid=small_empty_grid)
        assert state.generation == 0
        assert state.mode == SimulationMode.STOPPED
        assert state.speed_level == 3
        assert state.last_update_ms is None


class TestSimulationStateTransitions:
    """Tests for immutable state transition methods."""

    def test_with_grid(self, small_empty_grid: Grid) -> None:
        """with_grid returns new state with different grid."""
        state = SimulationState(current_grid=small_empty_grid)
        live = frozenset({(5, 5)})
        new_grid = Grid(width=10, height=10, live_cells=live)
        new_state = state.with_grid(new_grid)
        assert new_state.current_grid is new_grid
        assert new_state.generation == state.generation

    def test_advance_generation(self, small_empty_grid: Grid) -> None:
        """advance_generation increments generation and sets timestamp."""
        state = SimulationState(current_grid=small_empty_grid)
        new_state = state.advance_generation(small_empty_grid)
        assert new_state.generation == 1
        assert new_state.last_update_ms is not None

    def test_change_mode(self, small_empty_grid: Grid) -> None:
        """change_mode returns new state with different mode."""
        state = SimulationState(current_grid=small_empty_grid)
        running = state.change_mode(SimulationMode.RUNNING)
        assert running.mode == SimulationMode.RUNNING
        assert state.mode == SimulationMode.STOPPED  # Original unchanged

    def test_change_speed_valid(self, small_empty_grid: Grid) -> None:
        """change_speed with valid level returns new state."""
        state = SimulationState(current_grid=small_empty_grid)
        fast = state.change_speed(10)
        assert fast.speed_level == 10

    def test_change_speed_invalid_too_high(self, small_empty_grid: Grid) -> None:
        """change_speed > 10 raises InvalidSpeedLevelError."""
        state = SimulationState(current_grid=small_empty_grid)
        with pytest.raises(InvalidSpeedLevelError):
            state.change_speed(11)

    def test_change_speed_invalid_too_low(self, small_empty_grid: Grid) -> None:
        """change_speed < 1 raises InvalidSpeedLevelError."""
        state = SimulationState(current_grid=small_empty_grid)
        with pytest.raises(InvalidSpeedLevelError):
            state.change_speed(0)


class TestSimulationController:
    """Tests for the SimulationController class."""

    def test_initial_mode_is_stopped(
        self, stopped_simulation: SimulationController
    ) -> None:
        """Controller starts in STOPPED mode."""
        assert stopped_simulation.state.mode == SimulationMode.STOPPED

    def test_start(self, stopped_simulation: SimulationController) -> None:
        """start() transitions to RUNNING mode."""
        stopped_simulation.start()
        assert stopped_simulation.state.mode == SimulationMode.RUNNING

    def test_pause(self, running_simulation: SimulationController) -> None:
        """pause() transitions from RUNNING to PAUSED."""
        running_simulation.pause()
        assert running_simulation.state.mode == SimulationMode.PAUSED

    def test_stop(self, running_simulation: SimulationController) -> None:
        """stop() transitions to STOPPED mode."""
        running_simulation.stop()
        assert running_simulation.state.mode == SimulationMode.STOPPED

    def test_toggle_from_stopped(
        self, stopped_simulation: SimulationController
    ) -> None:
        """toggle() from STOPPED → RUNNING."""
        stopped_simulation.toggle()
        assert stopped_simulation.state.mode == SimulationMode.RUNNING

    def test_toggle_from_running(
        self, running_simulation: SimulationController
    ) -> None:
        """toggle() from RUNNING → PAUSED."""
        running_simulation.toggle()
        assert running_simulation.state.mode == SimulationMode.PAUSED

    def test_toggle_from_paused(self, stopped_simulation: SimulationController) -> None:
        """toggle() from PAUSED → RUNNING."""
        stopped_simulation.start()
        stopped_simulation.pause()
        stopped_simulation.toggle()
        assert stopped_simulation.state.mode == SimulationMode.RUNNING


class TestSpeedControl:
    """Tests for speed increase/decrease methods."""

    def test_increase_speed(self, stopped_simulation: SimulationController) -> None:
        """increase_speed() increments speed level by 1."""
        initial = stopped_simulation.state.speed_level
        stopped_simulation.increase_speed()
        assert stopped_simulation.state.speed_level == initial + 1

    def test_decrease_speed(self, stopped_simulation: SimulationController) -> None:
        """decrease_speed() decrements speed level by 1."""
        initial = stopped_simulation.state.speed_level
        stopped_simulation.decrease_speed()
        assert stopped_simulation.state.speed_level == initial - 1

    def test_increase_speed_caps_at_10(
        self, stopped_simulation: SimulationController
    ) -> None:
        """Speed cannot exceed level 10."""
        for _ in range(20):
            stopped_simulation.increase_speed()
        assert stopped_simulation.state.speed_level == 10

    def test_decrease_speed_caps_at_1(
        self, stopped_simulation: SimulationController
    ) -> None:
        """Speed cannot go below level 1."""
        for _ in range(20):
            stopped_simulation.decrease_speed()
        assert stopped_simulation.state.speed_level == 1


class TestGenerationAdvancement:
    """Tests for generation timing and advancement."""

    def test_should_advance_when_stopped(
        self, stopped_simulation: SimulationController
    ) -> None:
        """Should not advance when simulation is stopped."""
        assert not stopped_simulation.should_advance()

    def test_should_advance_when_paused(
        self, running_simulation: SimulationController
    ) -> None:
        """Should not advance when simulation is paused."""
        running_simulation.pause()
        assert not running_simulation.should_advance()

    def test_advance_increments_generation(
        self, running_simulation: SimulationController
    ) -> None:
        """advance() increments generation counter."""
        initial_gen = running_simulation.state.generation
        running_simulation.advance()
        assert running_simulation.state.generation == initial_gen + 1

    def test_advance_applies_conway_rules(self) -> None:
        """advance() properly applies Conway's rules to grid."""
        config = GameConfig(grid_width=10, grid_height=10)
        # Horizontal blinker
        live = frozenset({(5, 4), (5, 5), (5, 6)})
        grid = Grid(width=10, height=10, live_cells=live)
        controller = SimulationController(config=config, grid=grid)
        controller.start()
        controller.advance()
        # Should become vertical blinker
        new_grid = controller.state.current_grid
        assert new_grid.is_alive(4, 5)
        assert new_grid.is_alive(5, 5)
        assert new_grid.is_alive(6, 5)

    def test_update_grid(self, stopped_simulation: SimulationController) -> None:
        """update_grid() replaces current grid."""
        live = frozenset({(5, 5)})
        new_grid = Grid(width=10, height=10, live_cells=live)
        stopped_simulation.update_grid(new_grid)
        assert stopped_simulation.state.current_grid.population == 1

    def test_reset(self, running_simulation: SimulationController) -> None:
        """reset() sets generation to 0 and mode to STOPPED."""
        running_simulation.advance()
        empty = Grid.create_empty(10, 10)
        running_simulation.reset(empty)
        assert running_simulation.state.generation == 0
        assert running_simulation.state.mode == SimulationMode.STOPPED
        assert running_simulation.state.current_grid.population == 0


class TestGameConfig:
    """Tests for GameConfig validation and methods."""

    def test_default_config(self) -> None:
        """Default config has expected values."""
        config = GameConfig()
        assert config.grid_width == 50
        assert config.grid_height == 50
        assert config.cell_size == 12
        assert config.default_speed == 3

    def test_invalid_grid_width_too_small(self) -> None:
        """Grid width < 10 raises validation error."""
        with pytest.raises(Exception):
            GameConfig(grid_width=5)

    def test_invalid_grid_width_too_large(self) -> None:
        """Grid width > 200 raises validation error."""
        with pytest.raises(Exception):
            GameConfig(grid_width=201)

    def test_calculate_delay_for_speed_slowest(self) -> None:
        """Speed 1 gives maximum delay."""
        config = GameConfig()
        delay = config.calculate_delay_for_speed(1)
        assert delay == config.max_generation_delay_ms

    def test_calculate_delay_for_speed_fastest(self) -> None:
        """Speed 10 gives minimum delay."""
        config = GameConfig()
        delay = config.calculate_delay_for_speed(10)
        assert delay == config.min_generation_delay_ms

    def test_calculate_delay_monotonic(self) -> None:
        """Higher speed levels produce smaller delays."""
        config = GameConfig()
        delays = [config.calculate_delay_for_speed(i) for i in range(1, 11)]
        for i in range(len(delays) - 1):
            assert delays[i] >= delays[i + 1]

    def test_calculate_window_dimensions(self) -> None:
        """Window dimensions match grid_size * cell_size + panel."""
        config = GameConfig(grid_width=20, grid_height=15, cell_size=10)
        assert config.calculate_window_width() == 200
        assert config.calculate_window_height() == 15 * 10 + config.ui_panel_height

    def test_frozen_config(self) -> None:
        """GameConfig is immutable after creation."""
        config = GameConfig()
        with pytest.raises(Exception):
            config.grid_width = 100  # type: ignore[misc]

    def test_delay_ordering_validation(self) -> None:
        """max_generation_delay_ms must exceed min_generation_delay_ms."""
        with pytest.raises(Exception):
            GameConfig(max_generation_delay_ms=50, min_generation_delay_ms=100)
