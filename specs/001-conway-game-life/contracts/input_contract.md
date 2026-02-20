# Input Handling Contract

**Module**: `src/game/controls/`  
**Purpose**: Input processing and user interaction interface

## Interface: InputProcessor

```python
from typing import Protocol, List, Optional
import pygame

class InputProcessor(Protocol):
    """User input processing and event handling interface.
    
    Converts raw pygame events into normalized InputEvent objects
    for consumption by game logic layers.
    """
    
    def process_events(self, pygame_events: List[pygame.event.Event]) -> List[InputEvent]:
        """Convert pygame events to normalized input events.
        
        Args:
            pygame_events: Raw pygame event list from event queue
            
        Returns:
            List of normalized InputEvent objects for game processing
        """
        ...
    
    def process_mouse_click(self, mouse_pos: Tuple[int, int], display_state: DisplayState) -> Optional[InputEvent]:
        """Convert mouse click to cell interaction event.
        
        Args:
            mouse_pos: Pixel coordinates of mouse click
            display_state: Current display configuration for coordinate conversion
            
        Returns:
            InputEvent for cell click, or None if click outside grid
        """
        ...
    
    def process_keyboard(self, key_event: pygame.event.Event) -> Optional[InputEvent]:
        """Convert keyboard input to control/speed events.
        
        Supported keys:
        - SPACE: Toggle simulation start/pause
        - PLUS/EQUALS: Increase speed
        - MINUS: Decrease speed  
        - C: Clear grid
        - ESCAPE/Q: Quit application
        
        Args:
            key_event: pygame keyboard event
            
        Returns:
            InputEvent for recognized keys, None for unhandled keys
        """
        ...
    
    def is_quit_requested(self, pygame_events: List[pygame.event.Event]) -> bool:
        """Check if user requested application termination.
        
        Args:
            pygame_events: Raw pygame event list
            
        Returns:
            True if quit was requested (window close, ESC, etc.)
        """
        ...

## Interface: UIControlManager

```python
class UIControlManager(Protocol):
    """UI button and control element management.
    
    Handles clickable UI elements separate from grid interaction.
    """
    
    def create_ui_buttons(self, config: GameConfig) -> List[UIButton]:
        """Initialize UI control buttons with positions and callbacks.
        
        Args:
            config: Game configuration for UI layout
            
        Returns:
            List of UIButton objects with screen positions
        """
        ...
    
    def handle_ui_click(self, mouse_pos: Tuple[int, int], buttons: List[UIButton]) -> Optional[InputEvent]:
        """Process mouse click on UI control elements.
        
        Args:
            mouse_pos: Pixel coordinates of mouse click
            buttons: Active UI button list
            
        Returns:
            InputEvent if button was clicked, None otherwise
        """
        ...
    
    def render_buttons(self, surface: pygame.Surface, buttons: List[UIButton], sim_state: SimulationState) -> None:
        """Render UI buttons with appropriate visual states.
        
        Args:
            surface: Target pygame surface for rendering
            buttons: UI button list to render
            sim_state: Current simulation state for button highlighting
        """
        ...

## Data Models

```python
@dataclass(frozen=True)
class UIButton:
    """UI button with position and action.
    
    Attributes:
        label: Display text for button
        x: Pixel x-coordinate of button
        y: Pixel y-coordinate of button 
        width: Button width in pixels
        height: Button height in pixels
        action_type: Type of InputEvent to generate when clicked
        action_data: Specific action data (ControlAction, SpeedAction, etc.)
    """
    label: str
    x: int
    y: int
    width: int
    height: int
    action_type: InputEventType
    action_data: Optional[Union[ControlAction, SpeedAction]] = None
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if pixel coordinates are within button bounds."""
        return (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )
    
    def to_input_event(self) -> InputEvent:
        """Generate InputEvent when button is activated."""
        if self.action_type == InputEventType.SIMULATION_CONTROL:
            return InputEvent(
                event_type=self.action_type,
                control_action=self.action_data
            )
        elif self.action_type == InputEventType.SPEED_CHANGE:
            return InputEvent(
                event_type=self.action_type,
                speed_action=self.action_data
            )
        else:
            return InputEvent(event_type=self.action_type)
```

## Contract Tests

```python
def test_input_processing_contract(processor: InputProcessor):
    """Verify input processing interface compliance."""
    
    # Test keyboard mapping
    space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    input_event = processor.process_keyboard(space_event)
    
    assert input_event is not None
    assert input_event.event_type == InputEventType.SIMULATION_CONTROL
    assert input_event.control_action in [ControlAction.START, ControlAction.PAUSE]
    
    # Test quit detection
    quit_event = pygame.event.Event(pygame.QUIT)
    assert processor.is_quit_requested([quit_event]) == True
    
    # Test mouse coordinate conversion
    display_state = DisplayState(window_width=800, window_height=600, grid_offset_x=50, grid_offset_y=50)
    click_event = processor.process_mouse_click((100, 100), display_state)
    
    if click_event:  # Only if click is within grid
        assert click_event.event_type == InputEventType.CELL_CLICK
        assert click_event.cell_coord is not None
        assert len(click_event.cell_coord) == 2

def test_ui_button_contract(ui_manager: UIControlManager, config: GameConfig):
    """Verify UI control management interface."""
    
    buttons = ui_manager.create_ui_buttons(config)
    assert len(buttons) > 0
    
    # Test button click detection
    for button in buttons:
        # Click center of button
        center_x = button.x + button.width // 2
        center_y = button.y + button.height // 2
        
        click_result = ui_manager.handle_ui_click((center_x, center_y), buttons)
        assert click_result is not None
        assert click_result.event_type == button.action_type
```

## Input Event Mapping

### Keyboard Shortcuts
- **SPACE**: Toggle simulation (START if stopped/paused, PAUSE if running)
- **+/=**: Increase simulation speed
- **-**: Decrease simulation speed
- **C**: Clear all cells (set grid to empty state)
- **ESC/Q**: Request application quit

### Mouse Interactions  
- **Left Click on Grid Cell**: Toggle cell state (alive ↔ dead)
- **Left Click on UI Button**: Execute button action
- **Window Close Button**: Request application quit

### UI Button Layout
- **Start/Pause Button**: Toggle simulation execution
- **Stop Button**: Stop simulation and reset to generation 0
- **Speed - Button**: Decrease simulation speed
- **Speed + Button**: Increase simulation speed  
- **Clear Button**: Clear all cells from grid

## Performance Requirements

- `process_events()` must handle 100+ events per frame without lag
- `process_mouse_click()` must complete coordinate conversion in <5ms
- UI button hit testing must be O(1) or O(n) with small n (<10 buttons)
- Event processing must not allocate significant memory per frame

## Error Handling

```python
class InputError(Exception):
    """Base exception for input processing failures."""
    
class InvalidCoordinateError(InputError):
    """Raised when coordinate conversion fails."""
    
class UILayoutError(InputError):
    """Raised when UI button layout is invalid."""
```