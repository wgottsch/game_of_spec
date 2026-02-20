"""Shared test fixtures and utilities for Conway's Game of Life tests.

Provides reusable fixtures for common test scenarios including
empty grids, known patterns, simulation states, and configuration.
"""

from typing import FrozenSet, Set, Tuple

import pytest

from game.config.settings import GameConfig
from game.core.cell import Cell
from game.core.grid import Grid
from game.core.simulation import SimulationController, SimulationMode, SimulationState

# ---------------------------------------------------------------------------
# Configuration fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def default_config() -> GameConfig:
    """Provide a default GameConfig for testing.

    Returns:
        GameConfig with default values (50x50 grid, 12px cells).
    """
    return GameConfig()


@pytest.fixture
def small_config() -> GameConfig:
    """Provide a small GameConfig for fast tests.

    Returns:
        GameConfig with 10x10 grid and 10px cells.
    """
    return GameConfig(grid_width=10, grid_height=10, cell_size=10)


# ---------------------------------------------------------------------------
# Grid fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def empty_grid() -> Grid:
    """Provide an empty 20x20 grid with no living cells.

    Returns:
        Empty Grid instance.
    """
    return Grid.create_empty(20, 20)


@pytest.fixture
def small_empty_grid() -> Grid:
    """Provide an empty 10x10 grid.

    Returns:
        Empty 10x10 Grid instance.
    """
    return Grid.create_empty(10, 10)


@pytest.fixture
def blinker_grid() -> Grid:
    """Provide a grid with a blinker pattern (period-2 oscillator).

    The blinker alternates between horizontal and vertical:
      Phase 1 (horizontal):  . X .     Phase 2 (vertical):  . . .
                              . X .                          X X X
                              . X .                          . . .

    Placed at rows 4-6, col 5 (vertical phase).

    Returns:
        Grid with a blinker pattern centered at (5, 5).
    """
    live: FrozenSet[Tuple[int, int]] = frozenset({(4, 5), (5, 5), (6, 5)})
    return Grid(width=20, height=20, live_cells=live)


@pytest.fixture
def glider_grid() -> Grid:
    """Provide a grid with a glider pattern (moving spaceship).

    Standard glider moving southeast:
      . X .
      . . X
      X X X

    Placed at rows 1-3, cols 1-3.

    Returns:
        Grid with a glider in the top-left area.
    """
    live: FrozenSet[Tuple[int, int]] = frozenset(
        {
            (1, 2),  # row 1, col 2
            (2, 3),  # row 2, col 3
            (3, 1),
            (3, 2),
            (3, 3),  # row 3, cols 1-3
        }
    )
    return Grid(width=20, height=20, live_cells=live)


@pytest.fixture
def block_grid() -> Grid:
    """Provide a grid with a block pattern (still life).

    A 2x2 block that remains unchanged between generations:
      X X
      X X

    Placed at rows 5-6, cols 5-6.

    Returns:
        Grid with a stable block pattern.
    """
    live: FrozenSet[Tuple[int, int]] = frozenset(
        {
            (5, 5),
            (5, 6),
            (6, 5),
            (6, 6),
        }
    )
    return Grid(width=20, height=20, live_cells=live)


@pytest.fixture
def beacon_grid() -> Grid:
    """Provide a grid with a beacon pattern (period-2 oscillator).

    Two overlapping blocks that oscillate:
      X X . .
      X X . .
      . . X X
      . . X X

    Placed at rows 4-7, cols 4-7.

    Returns:
        Grid with a beacon oscillator.
    """
    live: FrozenSet[Tuple[int, int]] = frozenset(
        {
            (4, 4),
            (4, 5),
            (5, 4),
            (5, 5),
            (6, 6),
            (6, 7),
            (7, 6),
            (7, 7),
        }
    )
    return Grid(width=20, height=20, live_cells=live)


@pytest.fixture
def toad_grid() -> Grid:
    """Provide a grid with a toad pattern (period-2 oscillator).

    Three-cell offset oscillator:
      . X X X
      X X X .

    Placed at rows 5-6, cols 4-6/5-7.

    Returns:
        Grid with a toad oscillator.
    """
    live: FrozenSet[Tuple[int, int]] = frozenset(
        {
            (5, 5),
            (5, 6),
            (5, 7),
            (6, 4),
            (6, 5),
            (6, 6),
        }
    )
    return Grid(width=20, height=20, live_cells=live)


# ---------------------------------------------------------------------------
# Simulation fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def stopped_simulation(
    small_config: GameConfig, small_empty_grid: Grid
) -> SimulationController:
    """Provide a stopped SimulationController with empty grid.

    Returns:
        SimulationController in STOPPED mode.
    """
    return SimulationController(config=small_config, grid=small_empty_grid)


@pytest.fixture
def running_simulation(
    small_config: GameConfig, blinker_grid: Grid
) -> SimulationController:
    """Provide a running SimulationController with blinker pattern.

    Returns:
        SimulationController in RUNNING mode with a blinker.
    """
    # Need a blinker grid that fits 10x10 config
    live: FrozenSet[Tuple[int, int]] = frozenset({(4, 5), (5, 5), (6, 5)})
    grid = Grid(width=10, height=10, live_cells=live)
    controller = SimulationController(config=small_config, grid=grid)
    controller.start()
    return controller
