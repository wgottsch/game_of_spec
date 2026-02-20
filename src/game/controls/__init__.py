"""Input handling and user interaction module.

Processes keyboard and mouse events, manages UI controls,
and converts raw pygame events into normalized InputEvent objects.
"""

from game.controls.events import (
    ControlAction,
    InputEvent,
    InputEventType,
    SpeedAction,
)

__all__ = [
    "InputEventType",
    "ControlAction",
    "SpeedAction",
    "InputEvent",
]
