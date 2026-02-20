"""Input event models for normalized event processing.

Defines enums and dataclasses for all user input events,
enabling type-safe event handling across module boundaries.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class InputEventType(Enum):
    """Categorized user input event types.

    Each type maps to a specific user action category
    that the game loop processes independently.
    """

    CELL_CLICK = "cell_click"
    SIMULATION_CONTROL = "simulation_control"
    SPEED_CHANGE = "speed_change"
    CLEAR_GRID = "clear_grid"
    QUIT_REQUEST = "quit_request"


class ControlAction(Enum):
    """Simulation control commands for start/pause/stop.

    Maps to keyboard shortcuts and UI button actions
    that change the simulation execution state.
    """

    START = "start"
    PAUSE = "pause"
    STOP = "stop"
    TOGGLE = "toggle"  # Toggle between start and pause


class SpeedAction(Enum):
    """Speed adjustment commands for +/- controls.

    Maps to keyboard shortcuts and UI button actions
    that change the simulation speed level.
    """

    INCREASE = "increase"
    DECREASE = "decrease"


@dataclass(frozen=True)
class InputEvent:
    """Normalized input event for cross-module communication.

    Wraps raw pygame events into a typed, validated structure
    that game logic can process without pygame dependency.

    Attributes:
        event_type: Category of the input event.
        cell_coord: Target cell (row, col) for CELL_CLICK events.
        control_action: Simulation command for SIMULATION_CONTROL events.
        speed_action: Speed direction for SPEED_CHANGE events.
    """

    event_type: InputEventType
    cell_coord: Optional[Tuple[int, int]] = None
    control_action: Optional[ControlAction] = None
    speed_action: Optional[SpeedAction] = None