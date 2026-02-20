# Core Game Logic Contract

**Module**: `src/game/core/`  
**Purpose**: Business logic interface for Conway's Game of Life rules

## Interface: GameEngine

```python
from abc import ABC, abstractmethod
from typing import Protocol

class GameEngine(Protocol):
    """Core Conway's Game of Life business logic interface.
    
    Responsible for rule application, grid management, and simulation state.
    Must be completely independent of display/input concerns.
    """
    
    def create_grid(self, width: int, height: int) -> Grid:
        """Create new empty grid with specified dimensions.
        
        Args:
            width: Grid width in cells (10-200)
            height: Grid height in cells (10-200)
            
        Returns:
            New Grid instance with all cells dead
            
        Raises:
            ValueError: If dimensions are invalid
        """
        ...
    
    def apply_conway_rules(self, grid: Grid) -> Grid:
        """Generate next grid state using Conway's Game of Life rules.
        
        Rules:
        - Live cell with 2-3 neighbors survives  
        - Dead cell with exactly 3 neighbors becomes alive
        - All other cells die or remain dead
        
        Args:
            grid: Current grid state
            
        Returns:
            New Grid instance representing next generation
        """
        ...
    
    def toggle_cell(self, grid: Grid, row: int, col: int) -> Grid:
        """Toggle cell state at specified coordinates.
        
        Args:
            grid: Current grid state
            row: Target cell row (0-based)
            col: Target cell column (0-based)
            
        Returns:
            New Grid instance with cell state toggled
            
        Raises:
            IndexError: If coordinates are outside grid bounds
        """
        ...
    
    def clear_grid(self, grid: Grid) -> Grid:
        """Return grid with all cells set to dead state.
        
        Args:
            grid: Grid to clear
            
        Returns:
            New Grid instance with all cells dead
        """
        ...
    
    def count_live_neighbors(self, grid: Grid, row: int, col: int) -> int:
        """Count living neighbors for cell at coordinates.
        
        Handles boundary conditions (cells outside grid are dead).
        
        Args:
            grid: Current grid state
            row: Cell row coordinate
            col: Cell column coordinate  
            
        Returns:
            Number of living neighbors (0-8)
        """
        ...

## Interface: SimulationController

```python
class SimulationController(Protocol):
    """Simulation timing and state management interface.
    
    Manages generation advancement, timing, and execution state
    without direct knowledge of rendering or input handling.
    """
    
    def create_simulation(self, initial_grid: Grid, config: GameConfig) -> SimulationState:
        """Initialize new simulation with grid and configuration.
        
        Args:
            initial_grid: Starting grid state
            config: Game configuration and timing settings
            
        Returns:
            New SimulationState in STOPPED mode at generation 0
        """
        ...
    
    def start_simulation(self, state: SimulationState) -> SimulationState:
        """Transition simulation to RUNNING mode.
        
        Args:
            state: Current simulation state
            
        Returns:
            New SimulationState in RUNNING mode
        """
        ...
    
    def pause_simulation(self, state: SimulationState) -> SimulationState:
        """Transition simulation to PAUSED mode.
        
        Args:
            state: Current simulation state
            
        Returns:
            New SimulationState in PAUSED mode
        """
        ...
    
    def advance_generation(self, state: SimulationState, engine: GameEngine) -> SimulationState:
        """Advance simulation by one generation if timing allows.
        
        Args:
            state: Current simulation state
            engine: Game engine for rule application
            
        Returns:
            New SimulationState with advanced generation (if timing permits)
        """
        ...
    
    def change_speed(self, state: SimulationState, speed_delta: int) -> SimulationState:
        """Modify simulation speed within valid range.
        
        Args:
            state: Current simulation state  
            speed_delta: Speed change (-1 for slower, +1 for faster)
            
        Returns:
            New SimulationState with updated speed
        """
        ...
    
    def should_advance(self, state: SimulationState, current_time_ms: float) -> bool:
        """Determine if generation should advance based on timing.
        
        Args:
            state: Current simulation state
            current_time_ms: Current timestamp in milliseconds
            
        Returns:
            True if enough time has passed for next generation
        """
        ...

## Contract Tests

```python
def test_conway_rules_contract(engine: GameEngine):
    """Verify Conway's Game of Life rules are correctly implemented."""
    
    # Test still life (block pattern)
    grid = engine.create_grid(4, 4)
    grid = engine.toggle_cell(grid, 1, 1)  # Create 2x2 block
    grid = engine.toggle_cell(grid, 1, 2)
    grid = engine.toggle_cell(grid, 2, 1) 
    grid = engine.toggle_cell(grid, 2, 2)
    
    next_grid = engine.apply_conway_rules(grid)
    assert next_grid.live_cells == grid.live_cells  # Should be unchanged
    
    # Test oscillator (blinker pattern)
    grid = engine.create_grid(5, 5)
    grid = engine.toggle_cell(grid, 2, 1)  # Horizontal line
    grid = engine.toggle_cell(grid, 2, 2)
    grid = engine.toggle_cell(grid, 2, 3)
    
    next_grid = engine.apply_conway_rules(grid)
    expected_cells = {(1, 2), (2, 2), (3, 2)}  # Vertical line
    assert next_grid.live_cells == expected_cells

def test_simulation_timing_contract(controller: SimulationController, engine: GameEngine):
    """Verify simulation timing and state management."""
    
    config = GameConfig(grid_width=10, grid_height=10, default_speed=5)
    grid = engine.create_grid(10, 10)
    sim = controller.create_simulation(grid, config)
    
    # Test state transitions
    assert sim.mode == SimulationMode.STOPPED
    running_sim = controller.start_simulation(sim)
    assert running_sim.mode == SimulationMode.RUNNING
    
    paused_sim = controller.pause_simulation(running_sim)
    assert paused_sim.mode == SimulationMode.PAUSED
```

## Error Handling Requirements

```python
class GameLogicError(Exception):
    """Base exception for game logic violations."""
    
class InvalidGridDimensionsError(GameLogicError):
    """Raised when grid dimensions are invalid."""
    
class CellCoordinateError(GameLogicError):
    """Raised when cell coordinates are outside grid bounds."""
    
class InvalidSpeedLevelError(GameLogicError):
    """Raised when speed adjustment exceeds valid range."""

# All implementations must raise these specific exceptions
# rather than generic ValueError or IndexError
```

## Performance Requirements

- `apply_conway_rules()` must complete in <100ms for 200x200 grid
- `count_live_neighbors()` must be O(1) complexity (constant time lookup)
- `toggle_cell()` must complete in <10ms regardless of grid size
- Memory usage must not exceed 50MB for maximum grid configuration