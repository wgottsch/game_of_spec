"""Core business logic for Conway's Game of Life.

Contains game rules, grid management, and simulation control.
All game logic is independent of display and input handling.
"""

from game.core.exceptions import (
    CellCoordinateError,
    GameLogicError,
    InvalidGridDimensionsError,
    InvalidSpeedLevelError,
)

__all__ = [
    "GameLogicError",
    "InvalidGridDimensionsError",
    "CellCoordinateError",
    "InvalidSpeedLevelError",
]
