"""Pygame renderer for Conway's Game of Life.

Handles display initialization, grid cell rendering, UI panel drawing,
and coordinate conversion between pixel and grid space.
"""

from typing import List, Optional, Tuple

import pygame

from game.config.settings import GameConfig
from game.core.grid import Grid
from game.core.simulation import SimulationMode, SimulationState
from game.display import colors
from game.display.state import DisplayState


class GridRenderer:
    """Renders the game grid and UI elements using pygame.

    Manages the pygame display surface, draws living/dead cells,
    grid lines, the status panel, and UI buttons.

    Attributes:
        config: Game configuration for sizing and layout.
        display_state: Current display positioning and options.
        surface: Main pygame rendering surface.
        font: Primary font for UI text.
        small_font: Smaller font for secondary info.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialize the renderer and pygame display.

        Args:
            config: Game configuration with grid and display settings.
        """
        self.config = config

        # Calculate display dimensions and offsets
        window_width = config.calculate_window_width()
        window_height = config.calculate_window_height()
        self.display_state = DisplayState(
            window_width=window_width,
            window_height=window_height,
            grid_offset_x=0,
            grid_offset_y=0,
        )

        # Initialize pygame display
        pygame.init()
        self.surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(config.window_title)

        # Initialize fonts
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 14)

    def render_frame(
        self,
        grid: Grid,
        sim_state: SimulationState,
        mouse_pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Render a complete frame: background, grid, cells, UI.

        This is the main rendering entry point called once per frame
        in the game loop.

        Args:
            grid: Current grid state to render.
            sim_state: Current simulation state for status display.
            mouse_pos: Current mouse position for hover effects.
        """
        # Clear background
        self.surface.fill(colors.BACKGROUND)

        # Render grid cells and lines
        self._render_grid(grid, mouse_pos)

        # Render UI panel at the bottom
        self._render_ui_panel(sim_state)

        # Flip display buffer
        pygame.display.flip()

    def _render_grid(
        self,
        grid: Grid,
        mouse_pos: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Render the game grid with cells and grid lines.

        Draws dead cells as dark rectangles, live cells as bright rectangles,
        and subtle grid lines between all cells.

        Args:
            grid: Current grid state with live cell positions.
            mouse_pos: Mouse position for hover highlight effect.
        """
        cell_size = self.config.cell_size
        offset_x = self.display_state.grid_offset_x
        offset_y = self.display_state.grid_offset_y

        # Determine which cell the mouse hovers over (if any)
        hover_cell: Optional[Tuple[int, int]] = None
        if mouse_pos is not None:
            hover_result = self.pixel_to_grid_coord(mouse_pos[0], mouse_pos[1])
            if hover_result is not None:
                hover_cell = hover_result

        # Draw all cells — dead cells as subtle fill, live cells as bright fill
        for row in range(grid.height):
            for col in range(grid.width):
                x = offset_x + col * cell_size
                y = offset_y + row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)

                # Choose cell color based on state and hover
                if grid.is_alive(row, col):
                    color = colors.CELL_ALIVE
                elif hover_cell == (row, col):
                    color = colors.CELL_HOVER
                else:
                    color = colors.CELL_DEAD

                # Draw cell fill with 1px padding for grid line effect
                inner_rect = pygame.Rect(x + 1, y + 1, cell_size - 1, cell_size - 1)
                pygame.draw.rect(self.surface, color, inner_rect)

    def _render_ui_panel(self, sim_state: SimulationState) -> None:
        """Render the bottom UI panel with status and controls.

        Shows generation counter, simulation mode, speed level,
        and keyboard shortcut hints.

        Args:
            sim_state: Current simulation state for display values.
        """
        panel_y = self.config.grid_height * self.config.cell_size
        panel_rect = pygame.Rect(
            0, panel_y, self.display_state.window_width, self.config.ui_panel_height
        )

        # Draw panel background and top border
        pygame.draw.rect(self.surface, colors.UI_PANEL_BG, panel_rect)
        pygame.draw.line(
            self.surface,
            colors.UI_PANEL_BORDER,
            (0, panel_y),
            (self.display_state.window_width, panel_y),
            2,
        )

        # Mode indicator with color-coded text
        mode_text = sim_state.mode.value.upper()
        mode_color = {
            SimulationMode.RUNNING: colors.MODE_RUNNING,
            SimulationMode.PAUSED: colors.MODE_PAUSED,
            SimulationMode.STOPPED: colors.MODE_STOPPED,
        }.get(sim_state.mode, colors.STATUS_TEXT)

        mode_surface = self.font.render(mode_text, True, mode_color)
        self.surface.blit(mode_surface, (10, panel_y + 8))

        # Generation counter
        gen_text = f"Gen: {sim_state.generation}"
        gen_surface = self.font.render(gen_text, True, colors.GENERATION_TEXT)
        self.surface.blit(gen_surface, (140, panel_y + 8))

        # Speed indicator
        speed_text = f"Speed: {sim_state.speed_level}/10"
        speed_surface = self.font.render(speed_text, True, colors.SPEED_TEXT)
        self.surface.blit(speed_surface, (300, panel_y + 8))

        # Population counter
        pop_text = f"Pop: {sim_state.current_grid.population}"
        pop_surface = self.font.render(pop_text, True, colors.STATUS_TEXT)
        self.surface.blit(pop_surface, (460, panel_y + 8))

        # Keyboard shortcuts hint
        hint_text = "SPACE:Start/Pause  +/-:Speed  C:Clear  Q:Quit  Click:Toggle"
        hint_surface = self.small_font.render(hint_text, True, colors.STATUS_TEXT)
        self.surface.blit(hint_surface, (10, panel_y + 35))

    def pixel_to_grid_coord(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to grid cell coordinates.

        Args:
            x: Pixel x-coordinate (horizontal).
            y: Pixel y-coordinate (vertical).

        Returns:
            Tuple of (row, col) if within grid bounds, None otherwise.
        """
        cell_size = self.config.cell_size
        offset_x = self.display_state.grid_offset_x
        offset_y = self.display_state.grid_offset_y

        # Check if click is within grid area (above UI panel)
        grid_pixel_height = self.config.grid_height * cell_size
        if y < offset_y or y >= offset_y + grid_pixel_height:
            return None
        if x < offset_x or x >= offset_x + self.config.grid_width * cell_size:
            return None

        col = (x - offset_x) // cell_size
        row = (y - offset_y) // cell_size

        # Final bounds check
        if 0 <= row < self.config.grid_height and 0 <= col < self.config.grid_width:
            return (row, col)
        return None

    def calculate_cell_position(self, row: int, col: int) -> Tuple[int, int]:
        """Calculate pixel coordinates for a grid cell.

        Args:
            row: Cell row coordinate.
            col: Cell column coordinate.

        Returns:
            Tuple of (x, y) pixel coordinates for the cell's top-left corner.
        """
        x = self.display_state.grid_offset_x + col * self.config.cell_size
        y = self.display_state.grid_offset_y + row * self.config.cell_size
        return (x, y)

    def cleanup(self) -> None:
        """Clean up pygame resources.

        Should be called when the application is shutting down.
        """
        pygame.quit()
