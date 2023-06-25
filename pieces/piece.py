from abc import ABC, abstractmethod
from type import PieceType, TeamType


class Piece(ABC):
    """
    A parent class used to represent a Piece on a chessboard.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black)
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p', 'N', 'n').
        type (PieceType): The type of the piece (e.g., PAWN, KNIGHT).
    """
    
    def __init__(self, x: int, y: int, team: TeamType, is_white: bool, symbol: str, type: PieceType):
        """
        Initializes a Piece with a symbol, coordinates, type, and team.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black)
            symbol (str): The character symbol representing the piece (e.g., 'P', 'p', 'N', 'n').
            type (PieceType): The type of the piece (e.g., PAWN, KNIGHT).
        """
        self._x = x
        self._y = y
        self._team = team
        self._is_white = is_white
        self._symbol = symbol
        self._type = type
    
    @abstractmethod
    def legal_move(self, px: int, py: int, x: int, y: int):
        pass

    @property
    def x(self) -> int:
        """Returns the x-coordinate of the piece on the board."""
        return self._x

    @property
    def y(self) -> int:
        """Returns the y-coordinate of the piece on the board."""
        return self._y
    
    @x.setter
    def x(self, value: int):
        """
        Sets the x-coordinate of the piece on the board.

        Args:
            value (int): The new x-coordinate.
        """
        if not isinstance(value, int):
            raise TypeError("The x-coordinate must be an integer.")
        if not 0 <= value < 8:
            raise ValueError("The x-coordinate must be between 0 and 7.")
        self._x = value

    @y.setter
    def y(self, value: int):
        """
        Sets the y-coordinate of the piece on the board.

        Args:
            value (int): The new y-coordinate.
        """
        if not isinstance(value, int):
            raise TypeError("The y-coordinate must be an integer.")
        if not 0 <= value < 8:
            raise ValueError("The y-coordinate must be between 0 and 7.")
        self._y = value

    @property
    def team(self) -> TeamType:
        """Returns the team the piece belongs to."""
        return self._team
    
    @property
    def is_white(self) -> bool:
        """
        Returns the color of the piece.

        Returns:
            bool: True if the piece is white, False if the piece is black.
        """
        return self._is_white

    @property
    def symbol(self) -> str:
        """Returns the symbol of the piece."""
        return self._symbol
    
    @property
    def type(self) -> PieceType:
        """Returns the type of the piece."""
        return self._type
