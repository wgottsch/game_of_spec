"""Simulation controller for Conway's Game of Life.

Manages simulation state, timing, generation advancement, and mode
transitions. Operates independently of display and input modules.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from game.config.settings import GameConfig
from game.core.exceptions import InvalidSpeedLevelError
from game.core.grid import Grid


class SimulationMode(Enum):
    """Current simulation execution state.

    Determines how the simulation loop behaves — whether it advances
    automatically, waits for user input, or is fully stopped.
    """

    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


@dataclass(frozen=True)
class SimulationState:
    """Immutable snapshot of the complete simulation state.

    All state changes produce new instances to maintain immutability
    and enable clean state tracking throughout the game loop.

    Attributes:
        current_grid: The active grid configuration.
        generation: Current generation number (0 = initial state).
        mode: Simulation execution state (running/paused/stopped).
        speed_level: Speed multiplier on a 1-10 scale.
        last_update_ms: Timestamp of the last generation update (ms).
    """

    current_grid: Grid
    generation: int = 0
    mode: SimulationMode = SimulationMode.STOPPED
    speed_level: int = 3
    last_update_ms: Optional[float] = None

    def with_grid(self, new_grid: Grid) -> "SimulationState":
        """Return a new state with an updated grid.

        Args:
            new_grid: The replacement grid.

        Returns:
            New SimulationState with the new grid and reset generation.
        """
        return SimulationState(
            current_grid=new_grid,
            generation=self.generation,
            mode=self.mode,
            speed_level=self.speed_level,
            last_update_ms=self.last_update_ms,
        )

    def advance_generation(self, new_grid: Grid) -> "SimulationState":
        """Return a new state advanced by one generation.

        Args:
            new_grid: The grid after applying Conway's rules.

        Returns:
            New SimulationState with incremented generation and timestamp.
        """
        return SimulationState(
            current_grid=new_grid,
            generation=self.generation + 1,
            mode=self.mode,
            speed_level=self.speed_level,
            last_update_ms=time.time() * 1000,
        )

    def change_mode(self, new_mode: SimulationMode) -> "SimulationState":
        """Return a new state with a different execution mode.

        Args:
            new_mode: The desired simulation mode.

        Returns:
            New SimulationState with updated mode.
        """
        return SimulationState(
            current_grid=self.current_grid,
            generation=self.generation,
            mode=new_mode,
            speed_level=self.speed_level,
            last_update_ms=self.last_update_ms,
        )

    def change_speed(self, new_speed: int) -> "SimulationState":
        """Return a new state with a different speed level.

        Args:
            new_speed: Speed level from 1 (slowest) to 10 (fastest).

        Returns:
            New SimulationState with updated speed level.

        Raises:
            InvalidSpeedLevelError: If speed is outside 1-10 range.
        """
        if not (1 <= new_speed <= 10):
            raise InvalidSpeedLevelError(new_speed)
        return SimulationState(
            current_grid=self.current_grid,
            generation=self.generation,
            mode=self.mode,
            speed_level=new_speed,
            last_update_ms=self.last_update_ms,
        )


class SimulationController:
    """Manages simulation lifecycle and generation advancement.

    Provides high-level control over the simulation state, including
    starting, pausing, speed changes, and timed generation advancement.
    Uses immutable SimulationState for all state tracking.

    Attributes:
        config: Game configuration with timing parameters.
        state: Current immutable simulation state.
    """

    def __init__(self, config: GameConfig, grid: Grid) -> None:
        """Initialize the simulation controller.

        Args:
            config: Game configuration for timing and speed settings.
            grid: Initial grid state for the simulation.
        """
        self.config = config
        self.state = SimulationState(
            current_grid=grid,
            generation=0,
            mode=SimulationMode.STOPPED,
            speed_level=config.default_speed,
        )

    def start(self) -> None:
        """Start or resume the simulation.

        Transitions from STOPPED or PAUSED to RUNNING mode.
        Records the current timestamp for generation timing.
        """
        self.state = SimulationState(
            current_grid=self.state.current_grid,
            generation=self.state.generation,
            mode=SimulationMode.RUNNING,
            speed_level=self.state.speed_level,
            last_update_ms=time.time() * 1000,
        )

    def pause(self) -> None:
        """Pause the running simulation.

        Transitions from RUNNING to PAUSED mode, preserving all state.
        """
        self.state = self.state.change_mode(SimulationMode.PAUSED)

    def stop(self) -> None:
        """Stop the simulation completely.

        Transitions to STOPPED mode, preserving the current grid state.
        """
        self.state = self.state.change_mode(SimulationMode.STOPPED)

    def toggle(self) -> None:
        """Toggle between running and paused states.

        If running → pause. If paused or stopped → start.
        """
        if self.state.mode == SimulationMode.RUNNING:
            self.pause()
        else:
            self.start()

    def increase_speed(self) -> None:
        """Increase the simulation speed by one level (max 10).

        Silently caps at maximum speed level.
        """
        new_speed = min(10, self.state.speed_level + 1)
        self.state = self.state.change_speed(new_speed)

    def decrease_speed(self) -> None:
        """Decrease the simulation speed by one level (min 1).

        Silently caps at minimum speed level.
        """
        new_speed = max(1, self.state.speed_level - 1)
        self.state = self.state.change_speed(new_speed)

    def should_advance(self) -> bool:
        """Check if enough time has elapsed for the next generation.

        Compares elapsed time since last update against the delay
        calculated from the current speed level.

        Returns:
            True if the simulation should advance to the next generation.
        """
        if self.state.mode != SimulationMode.RUNNING:
            return False

        if self.state.last_update_ms is None:
            return True

        current_ms = time.time() * 1000
        delay = self.config.calculate_delay_for_speed(self.state.speed_level)
        elapsed = current_ms - self.state.last_update_ms
        return elapsed >= delay

    def advance(self) -> None:
        """Advance the simulation by one generation.

        Applies Conway's rules to the current grid and updates
        the simulation state with the new generation.
        """
        new_grid = self.state.current_grid.next_generation()
        self.state = self.state.advance_generation(new_grid)

    def update_grid(self, new_grid: Grid) -> None:
        """Replace the current grid (e.g., after cell toggle or clear).

        Args:
            new_grid: The replacement grid.
        """
        self.state = self.state.with_grid(new_grid)

    def reset(self, grid: Grid) -> None:
        """Fully reset the simulation with a new grid.

        Sets generation to 0, mode to STOPPED, and speed to default.

        Args:
            grid: The new starting grid.
        """
        self.state = SimulationState(
            current_grid=grid,
            generation=0,
            mode=SimulationMode.STOPPED,
            speed_level=self.config.default_speed,
        )
