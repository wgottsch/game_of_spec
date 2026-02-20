# Conway's Game of Life

A modular Python implementation of Conway's Game of Life with pygame visualization.
Business logic, grid management, and display are cleanly separated and independently testable.

## Prerequisites

- [mise](https://mise.jdx.dev/) — manages Python version and dev tools
- A graphical display (X11/Wayland) for pygame rendering

## Quick Start

```bash
# 1. Install Python 3.11 and uv via mise
mise install

# 2. Install all dependencies (creates .venv automatically)
uv sync

# 3. Run the game (prompts for grid dimensions)
uv run python src/main.py

# Or specify dimensions directly:
uv run python src/main.py 60 40
```

## Controls

| Key          | Action                      |
|--------------|-----------------------------|
| **SPACE**    | Start / Pause simulation    |
| **+** / **=**| Increase speed              |
| **-**        | Decrease speed              |
| **C**        | Clear grid                  |
| **Q** / ESC  | Quit application            |
| **Mouse click** | Toggle cell alive/dead   |

## Architecture

```
src/game/
├── core/           # Business logic (Conway's rules, simulation)
│   ├── cell.py     # Immutable Cell entity
│   ├── grid.py     # Grid with set-based live cells, rule engine
│   └── simulation.py # SimulationController, mode/speed management
├── display/        # Pygame visualization
│   ├── renderer.py # Grid and UI rendering
│   └── colors.py   # Color constants and theme
├── controls/       # Input handling
│   ├── input_handler.py # Keyboard/mouse → InputEvent conversion
│   └── ui_controls.py   # UI button management
└── config/         # Configuration
    └── settings.py # Pydantic-validated GameConfig
```

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=game --cov-report=term-missing

# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Type checking
uv run mypy src/game/
```

## Testing

- **Unit tests**: Cell, Grid, Simulation, Config, InputHandler, Colors
- **Integration tests**: Game flow lifecycle, UI input processing
- **Property-based tests**: Conway's B3/S23 rules verified with Hypothesis
- **Coverage target**: 80%+ for core business logic (achieved: 95%+)
