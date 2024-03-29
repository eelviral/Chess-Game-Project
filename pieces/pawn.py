from pieces import Piece
from utils.type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import ChessGame, GameEngine, Board


class Pawn(Piece):
    """
    Represents a Pawn piece in a chess game. Inherits from the Piece class.

    The Pawn class is a subclass of the Piece class, with a specific type of PieceType.PAWN.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p').
        type (PieceType): The type of the piece (PAWN).
    """

    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Pawn with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'P' if is_white else 'p'
        super().__init__(x, y, team, is_white, symbol, PieceType.PAWN)

    def legal_move(self, px: int, py: int, x: int, y: int, chess_game: 'ChessGame') -> bool:
        """
        Determine if a pawn's move is legal.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            chess_game (ChessGame): The chess game being played.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if self._moving_forward(px, py, x, y, board=chess_game.board) or \
                self._capturing(px, py, x, y, board=chess_game.board) or \
                self.en_passant(px, py, x, y, game_engine=chess_game.engine):
            return True
        else:
            return False

    def en_passant(self, px: int, py: int, x: int, y: int, game_engine: 'GameEngine') -> bool:
        """
        Check if the pawn is capturing by "en passant".

        En passant is a special pawn capture that can only occur immediately after a pawn
        moves two ranks forward from its starting position. The opponent captures the
        just-moved pawn "as it passes" through the first square.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_engine: (GameEngine): The chess game's engine.

        Returns:
            bool: True if the pawn is capturing by "en passant", False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        capture_rank = 3 if self.team == TeamType.ALLY else 4  # Decide the capture rank based on team

        last_move = game_engine.last_move
        if last_move is None:
            return False

        last_piece_moved, last_start_pos, last_end_pos = last_move
        if not isinstance(last_piece_moved, Pawn):  # Last piece moved must be a Pawn
            return False

        # Make sure the pawn can't capture allies
        if self.is_white == last_piece_moved.is_white:
            return False

        is_on_same_row = last_end_pos[1] == py
        is_directly_next_to_pawn = abs(last_end_pos[0] - px) == 1

        # The pawn must be beside this pawn
        if is_on_same_row and is_directly_next_to_pawn:
            # The pawn must have moved 2 steps
            if last_start_pos[1] - last_end_pos[1] == 2 * direction:
                # This pawn must be moving diagonally forward in the correct direction
                if py == capture_rank and dy == direction and dx == (last_end_pos[0] - px):
                    return True

        return False

    def is_controlled_square(self, current_x: int, current_y: int, target_x: int, target_y: int,
                             chess_game: 'ChessGame') -> bool:
        """
        Determine if a square is controlled by the Pawn.

        A Pawn controls the squares diagonally in front of it, depending on its color.

        Parameters:
            current_x (int): The current x-coordinate of this piece on the board.
            current_y (int): The current y-coordinate of this piece on the board.
            target_x (int): The x-coordinate of the proposed target square on the board.
            target_y (int): The y-coordinate of the proposed target square on the board.
            chess_game (ChessGame): The chess game being played.

        Returns:
            bool: True if the Pawn controls the target square, False otherwise.
        """
        dx = target_x - current_x
        dy = target_y - current_y
        direction = -1 if self.team == TeamType.ALLY else 1
        is_capture_square = (abs(dx) == 1 and dy == direction) and \
                self.can_capture_or_occupy_square(target_x, target_y, chess_game.board)

        return is_capture_square or \
            self.en_passant(px=current_x, py=current_y, x=target_x, y=target_y, game_engine=chess_game.engine)

    def _moving_forward(self, px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Check if the pawn is moving forward.

        The pawn moves straight forward one square, with the option to move two squares
        if it has not yet moved (pawn's first move). The pawn can't jump over pieces.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.

        Returns:
            bool: True if the pawn is moving forward correctly, False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        is_in_starting_position = (py == 6 if self.team == TeamType.ALLY else py == 1)

        if dx == 0 and dy == direction and board.piece_at(x, y) is None:
            return True
        elif dx == 0 and is_in_starting_position and dy == 2 * direction and \
                board.piece_at(x, y) is None and board.piece_at(px, py + direction) is None:
            return True
        else:
            return False

    def _capturing(self, px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Check if the pawn is capturing an opponent's piece.

        The pawn can capture an enemy piece on either of the two spaces adjacent to
        the space in front of it (diagonal forward), but cannot move to these spaces
        if they are vacant.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.

        Returns:
            bool: True if the pawn is capturing correctly, False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        return (abs(dx) == 1 and dy == direction) and \
            (board.piece_at(x, y) is not None and self.can_capture_or_occupy_square(x, y, board))
