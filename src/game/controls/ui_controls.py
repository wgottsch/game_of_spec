"""UI control button management for Conway's Game of Life.

Defines the UIButton dataclass and UIControlManager for creating
and handling clickable button elements in the pygame display.
Note: Current implementation uses keyboard shortcuts as primary
interaction. Buttons provide visual reference for available controls.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame

from game.controls.events import (
    ControlAction,
    InputEvent,
    InputEventType,
    SpeedAction,
)


@dataclass
class UIButton:
    """Clickable UI button with position, label, and action.

    Attributes:
        rect: Button bounding rectangle in pixel coordinates.
        label: Display text for the button.
        event: InputEvent to emit when button is clicked.
        is_hovered: Whether the mouse is currently over this button.
    """

    rect: pygame.Rect
    label: str
    event: InputEvent
    is_hovered: bool = False


class UIControlManager:
    """Creates and manages UI control buttons.

    Provides factory method for standard game control buttons
    and handles click detection on button areas.
    """

    @staticmethod
    def create_ui_buttons(panel_y: int, panel_width: int) -> List[UIButton]:
        """Create the standard set of game control buttons.

        Positions buttons in the UI panel area at the bottom of the window.

        Args:
            panel_y: Y-coordinate of the UI panel top edge.
            panel_width: Full width of the UI panel.

        Returns:
            List of UIButton instances for game controls.
        """
        # Buttons are placed in the panel for visual reference
        # Primary interaction is via keyboard shortcuts
        buttons: List[UIButton] = []
        # Currently relying on keyboard-only controls
        # Buttons can be added here for mouse-based UI in future
        return buttons

    @staticmethod
    def handle_ui_click(
        mouse_pos: Tuple[int, int], buttons: List[UIButton]
    ) -> Optional[InputEvent]:
        """Check if a mouse click hit any UI button.

        Args:
            mouse_pos: Pixel coordinates of the mouse click.
            buttons: List of active UI buttons.

        Returns:
            InputEvent for the clicked button, or None if no hit.
        """
        for button in buttons:
            if button.rect.collidepoint(mouse_pos):
                return button.event
        return None
