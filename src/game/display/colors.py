"""Color constants and theme management for the Game of Life display.

Centralizes all RGB color definitions to ensure consistent visual
appearance and easy theme customization.
"""

from typing import Tuple

# Type alias for RGB color tuples
Color = Tuple[int, int, int]

# ---------------------------------------------------------------------------
# Grid colors
# ---------------------------------------------------------------------------

# Background color for the entire window
BACKGROUND: Color = (25, 25, 35)

# Living cell fill color (bright green)
CELL_ALIVE: Color = (0, 200, 80)

# Dead cell fill color (dark gray, subtle)
CELL_DEAD: Color = (40, 40, 50)

# Grid line color (very subtle dark lines)
GRID_LINE: Color = (50, 50, 60)

# Cell hover highlight color (slightly brighter)
CELL_HOVER: Color = (80, 80, 100)

# ---------------------------------------------------------------------------
# UI panel colors
# ---------------------------------------------------------------------------

# UI panel background
UI_PANEL_BG: Color = (35, 35, 50)

# UI panel border/separator line
UI_PANEL_BORDER: Color = (70, 70, 90)

# Button normal state
BUTTON_NORMAL: Color = (60, 60, 80)

# Button hover state
BUTTON_HOVER: Color = (80, 80, 110)

# Button text color
BUTTON_TEXT: Color = (220, 220, 230)

# Status text color
STATUS_TEXT: Color = (180, 180, 200)

# Generation counter text color
GENERATION_TEXT: Color = (150, 200, 150)

# Speed indicator text color
SPEED_TEXT: Color = (200, 180, 100)

# Mode indicator: running (green)
MODE_RUNNING: Color = (0, 200, 80)

# Mode indicator: paused (yellow)
MODE_PAUSED: Color = (230, 200, 50)

# Mode indicator: stopped (red)
MODE_STOPPED: Color = (200, 60, 60)
