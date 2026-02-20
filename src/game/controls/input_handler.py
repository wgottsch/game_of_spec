"""Keyboard and mouse input handler for Conway's Game of Life.

Converts raw pygame events into normalized InputEvent objects,
enabling clean separation between input handling and game logic.
"""

from typing import List, Optional, Tuple

import pygame

from game.controls.events import (
    ControlAction,
    InputEvent,
    InputEventType,
    SpeedAction,
)
from game.display.state import DisplayState


class InputHandler:
    """Processes raw pygame events into normalized InputEvent objects.

    Maps keyboard shortcuts and mouse clicks to typed events that
    the game loop can process without direct pygame dependency.

    Keyboard mapping:
        SPACE    → Toggle start/pause
        +/=      → Increase speed
        -        → Decrease speed
        C        → Clear grid
        ESC / Q  → Quit application
    """

    def process_events(
        self,
        pygame_events: List[pygame.event.Event],
        pixel_to_grid_fn: Optional[object] = None,
    ) -> List[InputEvent]:
        """Convert a batch of pygame events to normalized InputEvents.

        Processes keyboard, mouse, and window events in a single pass.

        Args:
            pygame_events: Raw event list from pygame.event.get().
            pixel_to_grid_fn: Optional callable for coordinate conversion.

        Returns:
            List of normalized InputEvent objects for the game loop.
        """
        events: List[InputEvent] = []

        for event in pygame_events:
            if event.type == pygame.QUIT:
                events.append(InputEvent(event_type=InputEventType.QUIT_REQUEST))

            elif event.type == pygame.KEYDOWN:
                result = self.process_keyboard(event)
                if result is not None:
                    events.append(result)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left mouse click — handled externally via pixel_to_grid
                pass  # Coordinate conversion done in game loop

        return events

    def process_keyboard(self, key_event: pygame.event.Event) -> Optional[InputEvent]:
        """Convert a keyboard event into an InputEvent.

        Maps specific keys to simulation controls, speed changes,
        grid operations, and quit requests.

        Args:
            key_event: pygame KEYDOWN event.

        Returns:
            Corresponding InputEvent, or None for unmapped keys.
        """
        key = key_event.key

        # Simulation control: SPACE toggles start/pause
        if key == pygame.K_SPACE:
            return InputEvent(
                event_type=InputEventType.SIMULATION_CONTROL,
                control_action=ControlAction.TOGGLE,
            )

        # Speed increase: + or = key
        if key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            return InputEvent(
                event_type=InputEventType.SPEED_CHANGE,
                speed_action=SpeedAction.INCREASE,
            )

        # Speed decrease: - key
        if key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            return InputEvent(
                event_type=InputEventType.SPEED_CHANGE,
                speed_action=SpeedAction.DECREASE,
            )

        # Clear grid: C key
        if key == pygame.K_c:
            return InputEvent(event_type=InputEventType.CLEAR_GRID)

        # Quit: ESC or Q
        if key in (pygame.K_ESCAPE, pygame.K_q):
            return InputEvent(event_type=InputEventType.QUIT_REQUEST)

        return None

    def process_mouse_click(
        self,
        mouse_pos: Tuple[int, int],
        pixel_to_grid_fn: object,
    ) -> Optional[InputEvent]:
        """Convert a mouse click to a cell toggle event.

        Uses the provided coordinate conversion function to map
        pixel positions to grid cell coordinates.

        Args:
            mouse_pos: Pixel (x, y) of the mouse click.
            pixel_to_grid_fn: Callable that converts (x, y) → Optional[(row, col)].

        Returns:
            InputEvent with cell coordinates, or None if click outside grid.
        """
        # Call the converter to get grid coordinates
        grid_coord = pixel_to_grid_fn(mouse_pos[0], mouse_pos[1])  # type: ignore[operator]
        if grid_coord is not None:
            return InputEvent(
                event_type=InputEventType.CELL_CLICK,
                cell_coord=grid_coord,
            )
        return None

    @staticmethod
    def is_quit_requested(pygame_events: List[pygame.event.Event]) -> bool:
        """Quick check if any event is a quit request.

        Args:
            pygame_events: Raw pygame event list.

        Returns:
            True if window close or quit key was pressed.
        """
        for event in pygame_events:
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_ESCAPE,
                pygame.K_q,
            ):
                return True
        return False
