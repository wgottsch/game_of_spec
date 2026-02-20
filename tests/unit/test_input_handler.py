"""Unit tests for the InputHandler.

Tests keyboard mapping, event batch processing, and mouse click
coordinate conversion using mock pygame events.
"""

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


class TestInputHandlerKeyboard:
    """Tests for keyboard event to InputEvent mapping."""

    def setup_method(self) -> None:
        """Create a fresh InputHandler for each test."""
        self.handler = InputHandler()

    def test_space_key(self) -> None:
        """SPACE maps to SIMULATION_CONTROL TOGGLE."""
        event = MagicMock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.control_action == ControlAction.TOGGLE

    def test_numpad_plus(self) -> None:
        """Numpad + maps to speed increase."""
        event = MagicMock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_KP_PLUS
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.speed_action == SpeedAction.INCREASE

    def test_numpad_minus(self) -> None:
        """Numpad - maps to speed decrease."""
        event = MagicMock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_KP_MINUS
        result = self.handler.process_keyboard(event)
        assert result is not None
        assert result.speed_action == SpeedAction.DECREASE

    def test_unrecognized_key(self) -> None:
        """Unknown key returns None."""
        event = MagicMock(spec=pygame.event.Event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a
        result = self.handler.process_keyboard(event)
        assert result is None
