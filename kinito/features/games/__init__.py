"""Mini-games mixin: game picker and individual game launchers."""

from content import dialogue as dlg
from kinito.features.games.memory_ui import MemoryGame
from kinito.features.games.number_guess import new_secret_number
from kinito.features.games.tic_tac_toe import TicTacToeGame


class GamesMixin:
    """Offer and launch built-in mini-games."""

    def offer_game_picker(self):
        """Ask the user which mini-game to play."""
        if self._is_busy_with_speech():
            return
        self.speak(dlg.GAME_PICKER_QUESTION, 45, True)

    def speak_game_line(self, line, *, show_bubble=True):
        """Speak a game comment with TTS and show Kinito's speech bubble."""
        self.speak(line, show_bubble=show_bubble)

    def _ensure_single_game_window(self):
        """Close any open game window so only one game runs at a time."""
        window = getattr(self, "_game_window", None)
        if window is not None:
            try:
                if window.winfo_exists():
                    self._game_window = None
                    window.destroy()
            except Exception:
                self._game_window = None

    def start_tic_tac_toe(self):
        """Open a tic-tac-toe game window."""
        self.root.after(0, lambda: TicTacToeGame(self).open())

    def start_rock_paper_scissors(self):
        """Start a rock-paper-scissors round in the speech bubble."""
        self.speak(dlg.RPS_QUESTION, 45, True)

    def start_number_guess(self):
        """Start a number-guessing round."""
        self._number_guess_target = new_secret_number()
        self._number_guess_attempts = 0
        self.speak(dlg.NUMBER_GUESS_QUESTION, 45, True)

    def start_memory(self):
        """Open a memory card game window."""
        self.root.after(0, lambda: MemoryGame(self).open())
