# Display & Rendering Contract

**Module**: `src/game/display/`  
**Purpose**: Pygame visualization interface for grid rendering and UI

## Interface: GridRenderer

```python
from abc import ABC, abstractmethod
from typing import Protocol, Tuple
import pygame

class GridRenderer(Protocol):
    """Grid visualization interface for pygame rendering.
    
    Responsible for converting Grid data structures into visual representation.
    Must be independent of game logic and input handling.
    """
    
    def initialize_display(self, config: GameConfig) -> pygame.Surface:
        """Initialize pygame display with specified configuration.
        
        Args:
            config: Game configuration with display settings
            
        Returns:
            Main pygame surface for rendering
            
        Raises:
            DisplayInitializationError: If pygame initialization fails
        """
        ...
    
    def render_grid(self, surface: pygame.Surface, grid: Grid, display_state: DisplayState) -> None:
        """Render complete grid to surface.
        
        Args:
            surface: Target pygame surface for rendering
            grid: Current grid state to visualize  
            display_state: Display configuration and offsets
        """
        ...
    
    def render_cell(self, surface: pygame.Surface, cell: Cell, display_state: DisplayState) -> None:
        """Render individual cell at calculated position.
        
        Args:
            surface: Target pygame surface
            cell: Cell to render with coordinates and state
            display_state: Display configuration for positioning
        """
        ...
    
    def render_ui_elements(self, surface: pygame.Surface, sim_state: SimulationState) -> None:
        """Render simulation controls and status information.
        
        Args:
            surface: Target pygame surface
            sim_state: Current simulation state for status display
        """
        ...
    
    def calculate_cell_position(self, row: int, col: int, display_state: DisplayState) -> Tuple[int, int]:
        """Calculate pixel coordinates for grid cell.
        
        Args:
            row: Cell row coordinate
            col: Cell column coordinate
            display_state: Display configuration with offsets and scaling
            
        Returns:
            Tuple of (x, y) pixel coordinates for cell rendering
        """
        ...
    
    def pixel_to_grid_coord(self, x: int, y: int, display_state: DisplayState) -> Tuple[int, int]:
        """Convert pixel coordinates to grid cell coordinates.
        
        Args:
            x: Pixel x-coordinate
            y: Pixel y-coordinate  
            display_state: Display configuration for inverse calculation
            
        Returns:
            Tuple of (row, col) grid coordinates
            
        Raises:
            CoordinateOutOfBoundsError: If pixel is outside grid area
        """
        ...

## Interface: ColorManager

```python
class ColorManager(Protocol):
    """Color theming and visual style management.
    
    Centralizes all color decisions for consistent visual appearance.
    """
    
    def get_live_cell_color(self) -> Tuple[int, int, int]:
        """Get RGB color for living cells.
        
        Returns:
            RGB tuple for live cell rendering
        """
        ...
    
    def get_dead_cell_color(self) -> Tuple[int, int, int]:
        """Get RGB color for dead cells.
        
        Returns:
            RGB tuple for dead cell rendering
        """
        ...
    
    def get_grid_line_color(self) -> Tuple[int, int, int]:
        """Get RGB color for grid boundary lines.
        
        Returns:
            RGB tuple for grid line rendering
        """
        ...
    
    def get_ui_background_color(self) -> Tuple[int, int, int]:
        """Get RGB color for UI background elements.
        
        Returns:
            RGB tuple for UI background rendering
        """
        ...

## Contract Tests

```python
def test_rendering_contract(renderer: GridRenderer, config: GameConfig):
    """Verify rendering interface compliance."""
    
    # Test display initialization
    surface = renderer.initialize_display(config)
    assert surface is not None
    assert surface.get_width() > 0
    assert surface.get_height() > 0
    
    # Test coordinate conversion consistency
    display_state = DisplayState(
        window_width=800, window_height=600,
        grid_offset_x=50, grid_offset_y=50
    )
    
    # Round-trip coordinate conversion
    row, col = 5, 7
    x, y = renderer.calculate_cell_position(row, col, display_state)
    converted_row, converted_col = renderer.pixel_to_grid_coord(x, y, display_state)
    
    assert converted_row == row
    assert converted_col == col

def test_color_consistency(color_manager: ColorManager):
    """Verify color interface provides valid RGB values."""
    
    colors = [
        color_manager.get_live_cell_color(),
        color_manager.get_dead_cell_color(), 
        color_manager.get_grid_line_color(),
        color_manager.get_ui_background_color()
    ]
    
    for color in colors:
        assert len(color) == 3  # RGB tuple
        assert all(0 <= c <= 255 for c in color)  # Valid RGB range
```

## Performance Requirements

- `render_grid()` must maintain 30+ FPS for 100x100 grid
- `calculate_cell_position()` must be O(1) complexity 
- `pixel_to_grid_coord()` must complete in <5ms
- Memory allocation during rendering must be minimal (no new surfaces per frame)

## Error Handling

```python
class DisplayError(Exception):
    """Base exception for display-related failures."""
    
class DisplayInitializationError(DisplayError):
    """Raised when pygame display cannot be initialized."""
    
class CoordinateOutOfBoundsError(DisplayError):
    """Raised when pixel coordinates are outside valid grid area."""
    
class RenderingError(DisplayError):
    """Raised when rendering operations fail."""
```