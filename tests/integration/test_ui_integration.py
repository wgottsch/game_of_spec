"""Integration tests for UI input processing.

Tests keyboard and mouse input processing without requiring
a live pygame display (using mock events).
"""

from typing import Optional, Tuple
from unittest.mock import MagicMock

import pygame
import pytest

from game.controls.events import (
    ControlAction,
    InputEvent,
    InputEventType,
    SpeedAction,
)
from game.controls.input_handler import InputHandler


# Helper to create mock pygame events
def make_key_event(key: int) -> pygame.event.Event:
    """Create a mock KEYDOWN pygame event.

    Args:
        key: pygame key constant (e.g., pygame.K_SPACE).

    Returns:
        Mock pygame Event with type KEYDOWN and the specified key.
    """
    event = MagicMock(spec=pygame.event.Event)
    event.type = pygame.KEYDOWN
    event.key = key
    return event


def make_quit_event() -> pygame.event.Event:
    """Create a mock QUIT pygame event.

    Returns:
        Mock pygame Event with type QUIT.
    """
    event = MagicMock(spec=pygame.event.Event)
    event.type = pygame.QUIT
    return event


def make_mouse_event(pos: Tuple[int, int]) -> pygame.event.Event:
    """Create a mock MOUSEBUTTONDOWN pygame event.

    Args:
        pos: Pixel position of the click.

    Returns:
        Mock pygame Event with type MOUSEBUTTONDOWN.
    """
    event = MagicMock(spec=pygame.event.Event)
    event.type = pygame.MOUSEBUTTONDOWN
    event.button = 1
    event.pos = pos
    return event


# ---------------------------------------------------------------------------
# Keyboard input tests
# ---------------------------------------------------------------------------


class TestKeyboardInput:
    """Tests for keyboard event processing."""

    def setup_method(self) -> None:
        """Create a fresh InputHandler for each test."""
        self.handler = InputHandler()

    def test_space_toggles_simulation(self) -> None:
        """SPACE key produces SIMULATION_CONTROL TOGGLE event."""
        event = make_key_event(pygame.K_SPACE)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.SIMULATION_CONTROL
        assert result.control_action == ControlAction.TOGGLE

    def test_plus_increases_speed(self) -> None:
        """Plus key produces SPEED_CHANGE INCREASE event."""
        event = make_key_event(pygame.K_PLUS)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.SPEED_CHANGE
        assert result.speed_action == SpeedAction.INCREASE

    def test_equals_increases_speed(self) -> None:
        """Equals key (shift-agnostic plus) produces speed increase."""
        event = make_key_event(pygame.K_EQUALS)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.speed_action == SpeedAction.INCREASE

    def test_minus_decreases_speed(self) -> None:
        """Minus key produces SPEED_CHANGE DECREASE event."""
        event = make_key_event(pygame.K_MINUS)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.SPEED_CHANGE
        assert result.speed_action == SpeedAction.DECREASE

    def test_c_clears_grid(self) -> None:
        """C key produces CLEAR_GRID event."""
        event = make_key_event(pygame.K_c)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.CLEAR_GRID

    def test_escape_quits(self) -> None:
        """ESC key produces QUIT_REQUEST event."""
        event = make_key_event(pygame.K_ESCAPE)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.QUIT_REQUEST

    def test_q_quits(self) -> None:
        """Q key produces QUIT_REQUEST event."""
        event = make_key_event(pygame.K_q)
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.event_type == InputEventType.QUIT_REQUEST

    def test_unmapped_key_returns_none(self) -> None:
        """Unrecognized keys produce no event."""
        event = make_key_event(pygame.K_z)
        result = self.handler.process_keyboard(event)
        assert result is None


# ---------------------------------------------------------------------------
# Event batch processing tests
# ---------------------------------------------------------------------------


class TestEventBatchProcessing:
    """Tests for processing batches of pygame events."""

    def setup_method(self) -> None:
        """Create a fresh InputHandler for each test."""
        self.handler = InputHandler()

    def test_quit_event(self) -> None:
        """Window close event produces QUIT_REQUEST."""
        events = [make_quit_event()]
        results = self.handler.process_events(events)
        assert len(results) == 1
        assert results[0].event_type == InputEventType.QUIT_REQUEST

    def test_multiple_events(self) -> None:
        """Multiple events in one batch are all processed."""
        events = [
            make_key_event(pygame.K_SPACE),
            make_key_event(pygame.K_PLUS),
        ]
        results = self.handler.process_events(events)
        assert len(results) == 2
        assert results[0].event_type == InputEventType.SIMULATION_CONTROL
        assert results[1].event_type == InputEventType.SPEED_CHANGE

    def test_empty_event_list(self) -> None:
        """Empty event list returns empty result list."""
        results = self.handler.process_events([])
        assert results == []


# ---------------------------------------------------------------------------
# Mouse click coordinate conversion tests
# ---------------------------------------------------------------------------


class TestMouseClickProcessing:
    """Tests for mouse click to grid coordinate conversion."""

    def setup_method(self) -> None:
        """Create a fresh InputHandler for each test."""
        self.handler = InputHandler()

    def test_valid_click_produces_cell_event(self) -> None:
        """Click within grid produces CELL_CLICK event."""
        # Mock converter that always returns a valid coordinate
        converter = MagicMock(return_value=(5, 3))
        result = self.handler.process_mouse_click((100, 50), converter)
        assert result is not None
        assert result.event_type == InputEventType.CELL_CLICK
        assert result.cell_coord == (5, 3)

    def test_click_outside_grid_returns_none(self) -> None:
        """Click outside grid returns None."""
        converter = MagicMock(return_value=None)
        result = self.handler.process_mouse_click((999, 999), converter)
        assert result is None

    def test_converter_called_with_correct_coords(self) -> None:
        """Converter receives the exact pixel coordinates."""
        converter = MagicMock(return_value=(0, 0))
        self.handler.process_mouse_click((42, 77), converter)
        converter.assert_called_once_with(42, 77)


# ---------------------------------------------------------------------------
# Quit detection tests
# ---------------------------------------------------------------------------


class TestQuitDetection:
    """Tests for static quit check method."""

    def test_quit_event_detected(self) -> None:
        """QUIT event is detected by is_quit_requested."""
        events = [make_quit_event()]
        assert InputHandler.is_quit_requested(events) is True

    def test_escape_detected(self) -> None:
        """ESC key is detected as quit request."""
        events = [make_key_event(pygame.K_ESCAPE)]
        assert InputHandler.is_quit_requested(events) is True

    def test_q_detected(self) -> None:
        """Q key is detected as quit request."""
        events = [make_key_event(pygame.K_q)]
        assert InputHandler.is_quit_requested(events) is True

    def test_no_quit_event(self) -> None:
        """Non-quit events return False."""
        events = [make_key_event(pygame.K_SPACE)]
        assert InputHandler.is_quit_requested(events) is False

    def test_empty_events(self) -> None:
        """Empty event list returns False."""
        assert InputHandler.is_quit_requested([]) is False
