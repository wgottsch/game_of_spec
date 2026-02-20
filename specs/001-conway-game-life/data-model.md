# Data Model: Conway's Game of Life

**Generated**: February 20, 2026  
**Phase**: 1 - Design Specification

## Core Entities

### Cell
**Purpose**: Represents individual grid unit with binary state

```python
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Cell:
    """Immutable cell with coordinates and state.
    
    Attributes:
        row: Zero-based row position in grid
        col: Zero-based column position in grid  
        is_alive: Current living state of the cell
    """
    row: int
    col: int
    is_alive: bool = False
    
    def coordinate(self) -> Tuple[int, int]:
        """Get cell coordinate as (row, col) tuple."""
        return (self.row, self.col)
```

### Grid
**Purpose**: Manages 2D collection of cells and rule application

```python
from dataclasses import dataclass
from typing import List, Set, Tuple, Iterator
import itertools

@dataclass(frozen=True)
class Grid:
    """Immutable grid representing complete game state.
    
    Attributes:
        width: Number of columns in grid
        height: Number of rows in grid
        live_cells: Set of coordinates for currently living cells
    """
    width: int
    height: int
    live_cells: Set[Tuple[int, int]]
    
    def get_cell(self, row: int, col: int) -> Cell:
        """Get cell at specified coordinates."""
        
    def set_cell(self, row: int, col: int, is_alive: bool) -> 'Grid':
        """Return new grid with cell state modified."""
        
    def get_neighbors(self, row: int, col: int) -> List[Cell]:
        """Get all valid neighboring cells."""
        
    def count_live_neighbors(self, row: int, col: int) -> int:
        """Count living neighbors for Conway's rule application."""
        
    def next_generation(self) -> 'Grid':
        """Apply Conway's rules to generate next grid state."""
```

### SimulationState
**Purpose**: Tracks simulation execution and timing

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class SimulationMode(Enum):
    """Current simulation execution state."""
    STOPPED = "stopped"
    RUNNING = "running" 
    PAUSED = "paused"

@dataclass(frozen=True)
class SimulationState:
    """Complete simulation state with timing and controls.
    
    Attributes:
        current_grid: Active grid configuration
        generation: Current generation number
        mode: Simulation execution state
        speed_level: Speed multiplier (1-10 scale)
        last_update_ms: Timestamp of last generation update
    """
    current_grid: Grid
    generation: int
    mode: SimulationMode
    speed_level: int
    last_update_ms: Optional[float] = None
    
    def with_grid(self, new_grid: Grid) -> 'SimulationState':
        """Return new state with updated grid."""
        
    def advance_generation(self) -> 'SimulationState':
        """Return new state with advanced generation."""
        
    def change_mode(self, new_mode: SimulationMode) -> 'SimulationState':
        """Return new state with different execution mode."""
```

### GameConfig  
**Purpose**: Validated configuration and runtime settings

```python
from pydantic import BaseModel, Field, validator

class GameConfig(BaseModel):
    """Immutable game configuration with validation.
    
    All settings are validated at initialization and remain constant
    throughout application execution.
    """
    
    # Grid Configuration
    grid_width: int = Field(ge=10, le=200, description="Grid width in cells")
    grid_height: int = Field(ge=10, le=200, description="Grid height in cells")
    
    # Display Configuration  
    cell_size: int = Field(ge=3, le=20, description="Cell size in pixels")
    window_title: str = "Conway's Game of Life"
    target_fps: int = Field(ge=10, le=120, default=60)
    
    # Simulation Configuration
    default_speed: int = Field(ge=1, le=10, default=3)
    max_generation_delay_ms: int = Field(ge=50, le=5000, default=500)
    min_generation_delay_ms: int = Field(ge=10, le=1000, default=50)
    
    @validator('grid_width', 'grid_height')
    def validate_grid_size(cls, v):
        """Ensure grid dimensions support minimum viable patterns."""
        if v < 10:
            raise ValueError("Grid must be at least 10x10 for meaningful patterns")
        return v
    
    class Config:
        """Pydantic configuration."""
        frozen = True  # Immutable after creation
        validate_assignment = True
```

## Display Models

### DisplayState
**Purpose**: Rendering-specific state and UI information

```python
@dataclass(frozen=True)
class DisplayState:
    """Current display and UI state.
    
    Attributes:  
        window_width: Rendered window width in pixels
        window_height: Rendered window height in pixels
        grid_offset_x: Grid rendering x-offset for centering
        grid_offset_y: Grid rendering y-offset for centering
        show_grid_lines: Whether to render grid boundaries
        selected_cell: Currently highlighted cell (if any)
    """
    window_width: int
    window_height: int  
    grid_offset_x: int
    grid_offset_y: int
    show_grid_lines: bool = True
    selected_cell: Optional[Tuple[int, int]] = None
```

### InputEvent
**Purpose**: Normalized input events for cross-module communication

```python
from enum import Enum
from dataclasses import dataclass

class InputEventType(Enum):
    """Categorized user input events."""
    CELL_CLICK = "cell_click"
    SIMULATION_CONTROL = "simulation_control" 
    SPEED_CHANGE = "speed_change"
    CLEAR_GRID = "clear_grid"
    QUIT_REQUEST = "quit_request"

class ControlAction(Enum):  
    """Simulation control commands."""
    START = "start"
    PAUSE = "pause" 
    STOP = "stop"
    
class SpeedAction(Enum):
    """Speed adjustment commands."""
    INCREASE = "increase"
    DECREASE = "decrease"

@dataclass(frozen=True)
class InputEvent:
    """Normalized input event for processing.
    
    Attributes:
        event_type: Category of input event
        cell_coord: Target cell coordinate (for CELL_CLICK)
        control_action: Simulation control (for SIMULATION_CONTROL)
        speed_action: Speed change direction (for SPEED_CHANGE)
    """
    event_type: InputEventType
    cell_coord: Optional[Tuple[int, int]] = None
    control_action: Optional[ControlAction] = None  
    speed_action: Optional[SpeedAction] = None
```

## Data Flow Architecture

### State Transitions
1. **Input Layer** → `InputEvent` → **Control Layer**
2. **Control Layer** → `SimulationState` modifications → **Core Layer**  
3. **Core Layer** → `Grid` transformations → **Display Layer**
4. **Display Layer** → `pygame.Surface` rendering → **Screen**

### Immutability Constraints
- All data models are frozen dataclasses or Pydantic models
- State changes create new instances rather than mutations
- Grid operations return new Grid instances with modifications
- Simulation advances return new SimulationState instances

### Type Safety Guarantees  
- All coordinates validated as `Tuple[int, int]`
- Cell states maintain boolean type consistency
- Speed levels constrained to valid integer ranges
- Configuration validation prevents invalid runtime states

### Performance Considerations
- Immutable data enables efficient change detection
- Set-based live_cells storage for O(1) lookup performance
- Coordinate-based algorithms avoid full grid iterations
- Shallow copying for unchanged data structures