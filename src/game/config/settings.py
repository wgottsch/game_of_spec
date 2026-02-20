"""Game configuration with Pydantic validation.

Provides immutable, validated configuration for grid dimensions,
display settings, and simulation parameters. All values are validated
at initialization and remain constant during application execution.
"""

from typing import Self

from pydantic import BaseModel, Field, model_validator


class GameConfig(BaseModel):
    """Immutable game configuration with comprehensive validation.

    All settings are validated at initialization. The model is frozen
    to prevent accidental mutation during runtime.

    Attributes:
        grid_width: Number of columns in the grid (10-200).
        grid_height: Number of rows in the grid (10-200).
        cell_size: Visual size of each cell in pixels (3-50).
        window_title: Title text for the pygame window.
        target_fps: Target frames per second for rendering (10-120).
        default_speed: Initial simulation speed level (1-10).
        max_generation_delay_ms: Slowest generation interval in ms.
        min_generation_delay_ms: Fastest generation interval in ms.
        ui_panel_height: Height of the bottom UI panel in pixels.
    """

    # Grid configuration
    grid_width: int = Field(
        default=50,
        ge=10,
        le=200,
        description="Grid width in cells (columns)",
    )
    grid_height: int = Field(
        default=50,
        ge=10,
        le=200,
        description="Grid height in cells (rows)",
    )

    # Display configuration
    cell_size: int = Field(
        default=12,
        ge=3,
        le=50,
        description="Cell size in pixels for rendering",
    )
    window_title: str = "Conway's Game of Life"
    target_fps: int = Field(
        default=60,
        ge=10,
        le=120,
        description="Target frames per second",
    )
    ui_panel_height: int = Field(
        default=60,
        ge=40,
        le=120,
        description="Height of the bottom UI panel in pixels",
    )

    # Simulation configuration
    default_speed: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Default simulation speed level",
    )
    max_generation_delay_ms: int = Field(
        default=1000,
        ge=50,
        le=5000,
        description="Slowest generation interval in milliseconds",
    )
    min_generation_delay_ms: int = Field(
        default=50,
        ge=10,
        le=1000,
        description="Fastest generation interval in milliseconds",
    )

    model_config = {
        "frozen": True,
        "validate_assignment": True,
    }

    @model_validator(mode="after")
    def validate_delay_ordering(self) -> Self:
        """Ensure max delay is greater than min delay.

        Returns:
            Self: Validated instance.

        Raises:
            ValueError: If max_generation_delay_ms <= min_generation_delay_ms.
        """
        if self.max_generation_delay_ms <= self.min_generation_delay_ms:
            raise ValueError(
                f"max_generation_delay_ms ({self.max_generation_delay_ms}) "
                f"must be greater than min_generation_delay_ms ({self.min_generation_delay_ms})"
            )
        return self

    def calculate_window_width(self) -> int:
        """Calculate window width based on grid and cell size.

        Returns:
            Window width in pixels.
        """
        return self.grid_width * self.cell_size

    def calculate_window_height(self) -> int:
        """Calculate total window height including UI panel.

        Returns:
            Window height in pixels (grid area + UI panel).
        """
        return self.grid_height * self.cell_size + self.ui_panel_height

    def calculate_delay_for_speed(self, speed_level: int) -> int:
        """Calculate generation delay in ms for a given speed level.

        Linearly interpolates between max and min delay based on
        the speed level (1 = slowest, 10 = fastest).

        Args:
            speed_level: Speed level from 1 (slowest) to 10 (fastest).

        Returns:
            Generation delay in milliseconds.
        """
        # Clamp speed to valid range
        clamped = max(1, min(10, speed_level))
        # Linear interpolation: level 1 → max delay, level 10 → min delay
        delay_range = self.max_generation_delay_ms - self.min_generation_delay_ms
        return self.max_generation_delay_ms - int(delay_range * (clamped - 1) / 9)
