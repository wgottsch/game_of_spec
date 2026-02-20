# Quickstart Guide: Conway's Game of Life

**Target Audience**: Developers implementing the Conway's Game of Life specification  
**Prerequisites**: Python 3.11+, basic familiarity with pygame and pytest

## Overview

This project implements Conway's Game of Life cellular automaton with separated concerns:
- **Core Logic** (`src/game/core/`): Conway's rules and grid management
- **Display** (`src/game/display/`): pygame visualization and rendering
- **Controls** (`src/game/controls/`): Input handling and UI interaction

## Quick Setup

### 1. Environment Setup

```bash
# Clone and navigate to project
git clone <repository-url>
cd conway-game-life

# Install mise (if not already installed)
# See https://mise.jdx.dev/getting-started.html
curl https://mise.run | sh

# Provision Python and uv via mise
mise install

# Create .venv and install all dependencies (from uv.lock)
uv sync
```

### 2. Run Application

```bash
# Launch Conway's Game of Life
uv run python src/main.py

# Follow prompts to set grid size (e.g., 50x50)
# Use mouse clicks to create patterns
# Press SPACE to start/pause simulation
```

### 3. Run Tests

```bash
# Execute full test suite
uv run pytest tests/ -v

# Run specific test categories
uv run pytest tests/unit/ -v           # Unit tests only
uv run pytest tests/integration/ -v    # Integration tests only
uv run pytest tests/property/ -v       # Property-based tests

# Check test coverage
uv run pytest --cov=src tests/ --cov-report=html
```

## Architecture Overview

### Module Structure

```text
src/game/
├── core/                    # Business Logic Layer
│   ├── cell.py             # Cell entity and coordinates
│   ├── grid.py             # Grid management and Conway's rules  
│   └── simulation.py       # Simulation timing and state
├── display/                 # Visualization Layer
│   ├── renderer.py         # Grid and UI rendering
│   └── colors.py           # Color themes and constants
├── controls/                # Input Layer
│   ├── input_handler.py    # Event processing and normalization
│   └── ui_controls.py      # UI button management
└── config/                  # Configuration Layer
    └── settings.py         # Game configuration and validation
```

### Data Flow

1. **User Input** → `InputProcessor` → `InputEvent`
2. **InputEvent** → `SimulationController` → `SimulationState` 
3. **SimulationState** → `GameEngine` → `Grid` (next generation)
4. **Grid** → `GridRenderer` → pygame display

## Key Implementation Patterns

### Immutable Data Structures

```python
# All core data models are immutable
@dataclass(frozen=True)
class Grid:
    width: int
    height: int
    live_cells: Set[Tuple[int, int]]
    
    def toggle_cell(self, row: int, col: int) -> 'Grid':
        """Return new Grid with cell toggled."""
        new_live_cells = self.live_cells.copy()
        coord = (row, col)
        
        if coord in new_live_cells:
            new_live_cells.remove(coord)
        else:
            new_live_cells.add(coord)
            
        return Grid(self.width, self.height, new_live_cells)
```

### Conway's Rule Implementation

```python
def apply_conway_rules(self, grid: Grid) -> Grid:
    """Apply Conway's Game of Life rules to generate next generation.
    
    Rules:
    - Live cell with 2-3 neighbors survives
    - Dead cell with exactly 3 neighbors becomes alive  
    - All other cells die or remain dead
    """
    new_live_cells = set()
    
    # Check all cells that could potentially change state
    candidates = self._get_candidate_cells(grid)
    
    for row, col in candidates:
        neighbor_count = self._count_live_neighbors(grid, row, col)
        is_currently_alive = (row, col) in grid.live_cells
        
        if is_currently_alive and neighbor_count in {2, 3}:
            new_live_cells.add((row, col))  # Survival
        elif not is_currently_alive and neighbor_count == 3:
            new_live_cells.add((row, col))  # Birth
        # Death: cell not added to new_live_cells
    
    return Grid(grid.width, grid.height, new_live_cells)
```

### Input Event Processing

```python
def process_events(self, pygame_events: List[pygame.event.Event]) -> List[InputEvent]:
    """Convert pygame events to normalized InputEvent objects."""
    input_events = []
    
    for event in pygame_events:
        if event.type == pygame.KEYDOWN:
            input_event = self._process_keyboard(event)
            if input_event:
                input_events.append(input_event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_event = self._process_mouse_click(event)
            if input_event:
                input_events.append(input_event)
    
    return input_events
```

## Testing Strategy

### Unit Tests

Test individual modules in isolation:

```python
def test_conway_blinker_pattern():
    """Test blinker oscillator pattern evolution."""
    engine = ConwayGameEngine()
    grid = engine.create_grid(5, 5)
    
    # Create horizontal blinker
    grid = engine.toggle_cell(grid, 2, 1)
    grid = engine.toggle_cell(grid, 2, 2) 
    grid = engine.toggle_cell(grid, 2, 3)
    
    # Advance one generation
    next_grid = engine.apply_conway_rules(grid)
    
    # Should become vertical blinker
    expected_cells = {(1, 2), (2, 2), (3, 2)}
    assert next_grid.live_cells == expected_cells
```

### Integration Tests

Test module interactions:

```python
def test_full_simulation_cycle():
    """Test complete simulation from input to display."""
    config = GameConfig(grid_width=10, grid_height=10)
    engine = ConwayGameEngine()
    controller = SimulationController()
    
    # Create simulation with pattern
    grid = engine.create_grid(10, 10)
    grid = engine.toggle_cell(grid, 5, 5)  # Add live cell
    
    sim_state = controller.create_simulation(grid, config)
    running_state = controller.start_simulation(sim_state)
    
    # Simulate time passage and generation advancement
    next_state = controller.advance_generation(running_state, engine)
    
    assert next_state.generation == running_state.generation + 1
```

### Property-Based Tests

Test Conway's rule properties with random grids:

```python
from hypothesis import given, strategies as st

@given(st.sets(st.tuples(st.integers(0, 19), st.integers(0, 19)), max_size=50))
def test_conway_rules_are_deterministic(live_cell_coords):
    """Conway's rules must produce identical results for identical inputs."""
    engine = ConwayGameEngine()
    grid = Grid(width=20, height=20, live_cells=live_cell_coords)
    
    # Apply rules twice
    result1 = engine.apply_conway_rules(grid)
    result2 = engine.apply_conway_rules(grid)
    
    # Results must be identical
    assert result1.live_cells == result2.live_cells
```

## Development Workflow

### Code Quality Checks

```bash
# Type checking
uv run mypy src/

# Code formatting
uv run black src/ tests/

# Linting
uv run pylint src/

# Import sorting
uv run isort src/ tests/
```

### Pre-commit Hooks

```bash
# Install pre-commit
uv run pre-commit install

# Hooks will run automatically on commit
# Or run manually: uv run pre-commit run --all-files
```

## Common Patterns

### Creating Known Patterns

```python
def create_glider(grid: Grid, start_row: int, start_col: int) -> Grid:
    """Create glider pattern at specified position."""
    glider_coords = [
        (start_row, start_col + 1),
        (start_row + 1, start_col + 2), 
        (start_row + 2, start_col),
        (start_row + 2, start_col + 1),
        (start_row + 2, start_col + 2)
    ]
    
    result_grid = grid
    for row, col in glider_coords:
        if 0 <= row < grid.height and 0 <= col < grid.width:
            result_grid = engine.toggle_cell(result_grid, row, col)
    
    return result_grid
```

### Performance Optimization

```python
# Efficient neighbor calculation using sets
def _get_candidate_cells(self, grid: Grid) -> Set[Tuple[int, int]]:
    """Get cells that could change state (live cells + their neighbors)."""
    candidates = set()
    
    for row, col in grid.live_cells:
        # Add live cell itself
        candidates.add((row, col))
        
        # Add all neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                    
                nr, nc = row + dr, col + dc
                if 0 <= nr < grid.height and 0 <= nc < grid.width:
                    candidates.add((nr, nc))
    
    return candidates
```

## Troubleshooting

### Common Issues

**Performance**: Large grids (>100x100) running slowly
- Solution: Optimize candidate cell calculation, use set operations

**Input lag**: Mouse clicks not registering properly  
- Solution: Check coordinate conversion logic in `pixel_to_grid_coord()`

**Visual glitches**: Cells not rendering correctly
- Solution: Verify cell position calculation and color management

**Test failures**: Property-based tests finding edge cases
- Solution: Review boundary conditions in Conway's rule implementation

### Debugging Tips

```python
# Add logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Log grid states
logger.debug(f"Grid generation {generation}: {len(grid.live_cells)} live cells")

# Visualize grid in console for debugging
def print_grid(grid: Grid) -> None:
    """Print ASCII representation of grid."""
    for row in range(grid.height):
        line = ""
        for col in range(grid.width):
            if (row, col) in grid.live_cells:
                line += "*"
            else:
                line += "."
        print(line)
```

## Next Steps

After completing the basic implementation:

1. **Add preset patterns**: Implement common Conway's Game of Life patterns
2. **Save/load functionality**: Persist grid states to files
3. **Performance optimization**: Implement sparse grid algorithms for large patterns
4. **Advanced UI**: Add pattern library, zoom controls, generation scrubbing
5. **Analysis features**: Add statistics tracking, pattern recognition