"""Main application entry point for Conway's Game of Life.

Initializes all game components, runs the main game loop,
and handles clean shutdown. Provides optional command-line
grid dimension configuration.
"""

import logging
import sys
from typing import Optional

import pygame

from game.config.logging_config import setup_logging
from game.config.settings import GameConfig
from game.controls.events import (
    ControlAction,
    InputEvent,
    InputEventType,
    SpeedAction,
)
from game.controls.input_handler import InputHandler
from game.core.grid import Grid
from game.core.simulation import SimulationController, SimulationMode
from game.display.renderer import GridRenderer

# Module-level logger
logger = logging.getLogger("game.main")


def prompt_grid_dimensions() -> tuple[int, int]:
    """Prompt the user for grid dimensions via terminal input.

    Validates that dimensions are within the allowed range (10-200).
    Re-prompts on invalid input until valid values are provided.

    Returns:
        Tuple of (width, height) as integers.
    """
    print("\n=== Conway's Game of Life ===")
    print("Enter grid dimensions (10-200, or press Enter for 50x50 default):\n")

    while True:
        try:
            width_input = input("Grid width  [50]: ").strip()
            width = int(width_input) if width_input else 50

            height_input = input("Grid height [50]: ").strip()
            height = int(height_input) if height_input else 50

            # Validate range
            if not (10 <= width <= 200):
                print(f"Width must be between 10 and 200 (got {width}). Try again.")
                continue
            if not (10 <= height <= 200):
                print(f"Height must be between 10 and 200 (got {height}). Try again.")
                continue

            return (width, height)

        except ValueError:
            print("Please enter valid integer values. Try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nUsing default 50x50 grid.")
            return (50, 50)


def calculate_cell_size(width: int, height: int) -> int:
    """Calculate an appropriate cell size based on grid dimensions.

    Ensures the window fits comfortably on screen by scaling cell size
    down for large grids and up for small grids.

    Args:
        width: Grid width in cells.
        height: Grid height in cells.

    Returns:
        Cell size in pixels (clamped to 3-50 range).
    """
    # Target a window around 800-1000px wide
    target_window_width = 900
    target_window_height = 700
    size_by_width = target_window_width // width
    size_by_height = target_window_height // height
    cell_size = min(size_by_width, size_by_height)
    # Clamp to valid range
    return max(3, min(50, cell_size))


def process_input_event(
    event: InputEvent,
    controller: SimulationController,
    renderer: GridRenderer,
) -> bool:
    """Process a single normalized input event.

    Dispatches the event to the appropriate controller method
    based on the event type.

    Args:
        event: Normalized input event to process.
        controller: Simulation controller for state changes.
        renderer: Grid renderer for coordinate conversion.

    Returns:
        True if the application should continue, False to quit.
    """
    if event.event_type == InputEventType.QUIT_REQUEST:
        return False

    elif event.event_type == InputEventType.SIMULATION_CONTROL:
        if event.control_action == ControlAction.TOGGLE:
            controller.toggle()
            logger.debug("Simulation toggled to %s", controller.state.mode.value)

    elif event.event_type == InputEventType.SPEED_CHANGE:
        if event.speed_action == SpeedAction.INCREASE:
            controller.increase_speed()
            logger.debug("Speed increased to %d", controller.state.speed_level)
        elif event.speed_action == SpeedAction.DECREASE:
            controller.decrease_speed()
            logger.debug("Speed decreased to %d", controller.state.speed_level)

    elif event.event_type == InputEventType.CLEAR_GRID:
        new_grid = controller.state.current_grid.clear()
        controller.reset(new_grid)
        logger.info("Grid cleared, simulation reset")

    elif event.event_type == InputEventType.CELL_CLICK:
        if event.cell_coord is not None:
            row, col = event.cell_coord
            grid = controller.state.current_grid
            if grid.is_valid_coordinate(row, col):
                new_grid = grid.toggle_cell(row, col)
                controller.update_grid(new_grid)
                logger.debug("Cell (%d,%d) toggled", row, col)

    return True


def run_game(config: Optional[GameConfig] = None) -> None:
    """Initialize and run the main game loop.

    Sets up all components, enters the game loop processing events
    and rendering frames, and handles clean shutdown.

    Args:
        config: Optional pre-built GameConfig. If None, prompts user.
    """
    setup_logging(logging.INFO)

    # Prompt for dimensions if no config provided
    if config is None:
        width, height = prompt_grid_dimensions()
        cell_size = calculate_cell_size(width, height)
        config = GameConfig(
            grid_width=width,
            grid_height=height,
            cell_size=cell_size,
        )

    logger.info(
        "Starting Game of Life: %dx%d grid, %dpx cells",
        config.grid_width,
        config.grid_height,
        config.cell_size,
    )

    # Initialize components
    grid = Grid.create_empty(config.grid_width, config.grid_height)
    controller = SimulationController(config=config, grid=grid)
    renderer = GridRenderer(config=config)
    input_handler = InputHandler()

    # Main game loop clock
    clock = pygame.time.Clock()
    running = True

    try:
        while running:
            # --- Event handling ---
            pygame_events = pygame.event.get()
            input_events = input_handler.process_events(pygame_events)

            # Handle mouse clicks separately (needs coordinate conversion)
            for event in pygame_events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_event = input_handler.process_mouse_click(
                        event.pos, renderer.pixel_to_grid_coord
                    )
                    if click_event is not None:
                        input_events.append(click_event)

            # Process all input events
            for input_event in input_events:
                if not process_input_event(input_event, controller, renderer):
                    running = False
                    break

            if not running:
                break

            # --- Simulation update ---
            if controller.should_advance():
                controller.advance()

            # --- Rendering ---
            mouse_pos = pygame.mouse.get_pos()
            renderer.render_frame(
                grid=controller.state.current_grid,
                sim_state=controller.state,
                mouse_pos=mouse_pos,
            )

            # Maintain target FPS
            clock.tick(config.target_fps)

    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
    finally:
        renderer.cleanup()
        logger.info("Game shut down cleanly")


def main() -> None:
    """Application entry point.

    Parses optional command-line arguments and starts the game.
    """
    # Simple CLI: main.py [width] [height]
    config: Optional[GameConfig] = None

    if len(sys.argv) == 3:
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
            cell_size = calculate_cell_size(width, height)
            config = GameConfig(
                grid_width=width,
                grid_height=height,
                cell_size=cell_size,
            )
        except (ValueError, Exception) as e:
            print(f"Invalid arguments: {e}")
            print("Usage: python -m game.main [width] [height]")
            sys.exit(1)

    run_game(config)


if __name__ == "__main__":
    main()
