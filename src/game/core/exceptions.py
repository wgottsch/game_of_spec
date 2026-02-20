"""Custom exception classes for Conway's Game of Life core logic.

Provides specific, meaningful exception types for all error conditions
in the game engine and simulation controller.
"""


class GameLogicError(Exception):
    """Base exception for all game logic errors.

    All custom exceptions in the core module inherit from this class,
    enabling broad exception catching when needed.
    """


class InvalidGridDimensionsError(GameLogicError):
    """Raised when grid dimensions are outside valid range (10-200).

    Attributes:
        width: The invalid width value.
        height: The invalid height value.
        message: Human-readable error description.
    """

    def __init__(self, width: int, height: int, message: str = "") -> None:
        """Initialize with invalid dimensions.

        Args:
            width: The invalid grid width.
            height: The invalid grid height.
            message: Optional custom error message.
        """
        self.width = width
        self.height = height
        if not message:
            message = (
                f"Invalid grid dimensions: {width}x{height}. "
                f"Both must be between 10 and 200."
            )
        super().__init__(message)


class CellCoordinateError(GameLogicError):
    """Raised when cell coordinates are outside grid bounds.

    Attributes:
        row: The invalid row coordinate.
        col: The invalid column coordinate.
        message: Human-readable error description.
    """

    def __init__(self, row: int, col: int, message: str = "") -> None:
        """Initialize with invalid coordinates.

        Args:
            row: The invalid row coordinate.
            col: The invalid column coordinate.
            message: Optional custom error message.
        """
        self.row = row
        self.col = col
        if not message:
            message = f"Cell coordinates ({row}, {col}) are outside grid bounds."
        super().__init__(message)


class InvalidSpeedLevelError(GameLogicError):
    """Raised when speed level is outside valid range (1-10).

    Attributes:
        speed_level: The invalid speed level value.
        message: Human-readable error description.
    """

    def __init__(self, speed_level: int, message: str = "") -> None:
        """Initialize with invalid speed level.

        Args:
            speed_level: The invalid speed level value.
            message: Optional custom error message.
        """
        self.speed_level = speed_level
        if not message:
            message = f"Invalid speed level: {speed_level}. Must be between 1 and 10."
        super().__init__(message)
