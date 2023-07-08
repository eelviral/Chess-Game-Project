import tkinter as tk
from pieces import Piece, Pawn
from utils import piece_classes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import ChessUI


class PromotionUI:
    """
    A class to handle the user interface for pawn promotion in a game of chess.

    Attributes:
        chess_ui (ChessUI): The main game user interface.
        _selected_promotion (Piece or None): The selected piece to promote to, if any.
    """

    def __init__(self, chess_ui: 'ChessUI', pawn: Pawn):
        """
        Initialize the PromotionUI instance.

        Args:
            chess_ui (ChessUI): The main game user interface.
            pawn (Pawn): The pawn piece to be promoted.
        """
        self.chess_ui = chess_ui
        self._selected_promotion = None  # Add a member to store the selected promotion
        
        self.create_promotion_screen()
        self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))  # Schedule the first check
        
    def create_promotion_screen(self):
        """
        Creates a promotion screen. The user can select the type of piece to promote to.
        """
        # Create a new window
        promotion_window = tk.Toplevel(self.chess_ui.root)

        # Set window title
        promotion_window.title("Promote Pawn")

        # Set window size
        promotion_window.geometry("300x200")
        
        # Center the window on the root canvas
        window_width = promotion_window.winfo_reqwidth()
        window_height = promotion_window.winfo_reqheight()
        position_x = int((self.chess_ui.root.winfo_screenwidth() / 2) - (window_width / 2))
        position_y = int((self.chess_ui.root.winfo_screenheight() / 2) - (window_height / 2))
        promotion_window.geometry(f"+{position_x}+{position_y}")

        # Create label
        label = tk.Label(promotion_window, text="Choose a piece to promote to:")
        label.pack()

        def select_piece(piece_selected: str):
            # Instead of returning the piece, set the selected_promotion member
            self.selected_promotion = piece_classes[piece_selected]
            promotion_window.destroy()

        # Piece options
        pieces = ['Queen', 'Rook', 'Bishop', 'Knight']
        # Create a button for each piece
        for piece_name in pieces:
            button = tk.Button(
                promotion_window,
                text=piece_name,
                command=lambda piece_selected=piece_name: select_piece(piece_selected)
            )
            button.pack()
            
    def wait_for_promotion(self, pawn: Pawn):
        """
        Wait for the selected_promotion to be set, then continue with the promotion.

        Args:
            pawn (Pawn): The pawn piece to be promoted.
        """
        if self.selected_promotion is None:  # if the promotion hasn't been selected yet, schedule the check again
            self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))  # checks every 100 ms
        else:
            promotion_piece = self.selected_promotion
            self.selected_promotion = None  # reset selected promotion
            self.chess_ui.game_state.promote(pawn, promotion_piece)
            self.chess_ui.update()  # update immediately after promotion

    @property
    def selected_promotion(self) -> Piece or None:
        """
        Get the selected promotion.

        Returns:
            Piece or None: The selected promotion piece, or None if no piece has been selected.
        """
        return self._selected_promotion

    @selected_promotion.setter
    def selected_promotion(self, piece: Piece or None):
        """
        Set the selected promotion.

        Args:
            piece (Piece or None): The selected promotion piece, or None to clear the selection.
        """
        self._selected_promotion = piece
