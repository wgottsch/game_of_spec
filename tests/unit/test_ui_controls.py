"""Unit tests for UIControlManager and UIButton.

Tests button creation and click detection.
"""

import pygame
import pytest

from game.controls.events import ControlAction, InputEvent, InputEventType
from game.controls.ui_controls import UIButton, UIControlManager


class TestUIButton:
    """Tests for UIButton dataclass."""

    def test_create_button(self) -> None:
        """UIButton can be created with required fields."""
        rect = pygame.Rect(10, 20, 100, 30)
        event = InputEvent(
            event_type=InputEventType.SIMULATION_CONTROL,
            control_action=ControlAction.TOGGLE,
        )
        button = UIButton(rect=rect, label="Start", event=event)
        assert button.label == "Start"
        assert button.is_hovered is False

    def test_button_hover_state(self) -> None:
        """UIButton hover state can be set."""
        rect = pygame.Rect(10, 20, 100, 30)
        event = InputEvent(event_type=InputEventType.CLEAR_GRID)
        button = UIButton(rect=rect, label="Clear", event=event, is_hovered=True)
        assert button.is_hovered is True


class TestUIControlManager:
    """Tests for UIControlManager methods."""

    def test_create_ui_buttons_returns_list(self) -> None:
        """create_ui_buttons returns a list."""
        buttons = UIControlManager.create_ui_buttons(panel_y=500, panel_width=800)
        assert isinstance(buttons, list)

    def test_handle_click_no_buttons(self) -> None:
        """Click handling with no buttons returns None."""
        result = UIControlManager.handle_ui_click((100, 510), [])
        assert result is None

    def test_handle_click_hit(self) -> None:
        """Click on a button returns its InputEvent."""
        rect = pygame.Rect(50, 500, 100, 30)
        event = InputEvent(
            event_type=InputEventType.SIMULATION_CONTROL,
            control_action=ControlAction.TOGGLE,
        )
        button = UIButton(rect=rect, label="Test", event=event)
        result = UIControlManager.handle_ui_click((75, 510), [button])
        assert result is not None
        assert result.event_type == InputEventType.SIMULATION_CONTROL

    def test_handle_click_miss(self) -> None:
        """Click outside all buttons returns None."""
        rect = pygame.Rect(50, 500, 100, 30)
        event = InputEvent(event_type=InputEventType.CLEAR_GRID)
        button = UIButton(rect=rect, label="Test", event=event)
        result = UIControlManager.handle_ui_click((200, 400), [button])
        assert result is None
