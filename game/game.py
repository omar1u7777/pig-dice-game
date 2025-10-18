"""Main game logic for the Pig dice game.

This module contains the Game class which orchestrates the entire game,
managing players, turns, dice rolling, and win conditions.
"""

from typing import Tuple, Optional
from .player import Player
from .dice_hand import DiceHand
from .intelligence import Intelligence, DifficultyLevel


class Game:
    """Main game controller for Pig dice game.

    This class manages the game state, player turns, dice rolling,
    and determines when the game ends. It also handles AI decision making.

    Attributes:
        _player1 (Player): First player
        _player2 (Player): Second player
        _current_player_index (int): Index of current player (0 or 1)
        _winning_score (int): Score needed to win
        _dice_hand (DiceHand): Dice used for rolling
        _game_started (bool): Whether game has been started
        _game_over (bool): Whether game is finished
        _winner (Optional[Player]): Winner of the game if finished
        _ai_intelligence (Intelligence): AI strategy handler
    """

    def __init__(self, player1: Player, player2: Player, winning_score: int = 100):
        """Initialize game with two players.

        Args:
            player1 (Player): First player
            player2 (Player): Second player
            winning_score (int): Score needed to win. Defaults to 100.
        """
        self._player1 = player1
        self._player2 = player2
        self._current_player_index = 0
        self._winning_score = winning_score
        self._dice_hand = DiceHand(1)  # Pig uses single die
        self._game_started = False
        self._game_over = False
        self._winner: Optional[Player] = None

        # AI intelligence for computer players
        self._ai_intelligence = Intelligence(DifficultyLevel.MEDIUM)

    def start_game(self) -> None:
        """Start or restart the game.

        Resets all game state and player scores to initial values.
        """
        self._game_started = True
        self._game_over = False
        self._winner = None
        self._current_player_index = 0

        # Reset all scores for both players
        for player in [self._player1, self._player2]:
            player.reset_scores()

    def roll_dice(self) -> int:
        """Roll dice for the current player.

        Implements the core Pig game rule: rolling a 1 ends the turn
        and loses all turn points, otherwise the roll is added to turn score.

        Returns:
            int: The dice roll result

        Raises:
            RuntimeError: If game not started or is over
        """
        if not self._game_started:
            raise RuntimeError("Game not started")
        if self._game_over:
            raise RuntimeError("Game is over")

        # Roll the single die (Pig game uses one die)
        results = self._dice_hand.roll()
        result = results[0]  # Get single die result

        current_player = self.get_current_player()

        if result == 1:
            # Pig rule: rolling 1 loses turn and all turn points
            current_player.lose_turn()
            self._switch_player()
        else:
            # Add roll to current turn score
            current_player.add_to_turn(result)

        return result

    def hold_turn(self) -> int:
        """Current player holds and banks their turn points.

        Adds turn score to total score and switches to next player.
        Checks for win condition after banking points.

        Returns:
            int: Points that were banked

        Raises:
            RuntimeError: If game not active
        """
        if not self._game_started:
            raise RuntimeError("Game not started")
        if self._game_over:
            raise RuntimeError("Game is over")

        current_player = self.get_current_player()
        banked = current_player.hold_turn()

        # Check for win condition
        if current_player.has_won(self._winning_score):
            self._game_over = True
            self._winner = current_player
        else:
            self._switch_player()

        return banked

    def get_current_player(self) -> Player:
        """Get the current player whose turn it is.

        Returns:
            Player: Current player object
        """
        return self._player1 if self._current_player_index == 0 else self._player2

    def get_players(self) -> Tuple[Player, Player]:
        """Get both players in the game.

        Returns:
            Tuple[Player, Player]: Tuple of (player1, player2)
        """
        return self._player1, self._player2

    def get_winning_score(self) -> int:
        """Get the score needed to win.

        Returns:
            int: Winning score threshold
        """
        return self._winning_score

    def is_game_over(self) -> bool:
        """Check if the game has ended.

        Returns:
            bool: True if game has ended
        """
        return self._game_over

    def get_winner(self) -> Optional[Player]:
        """Get the winner if game is over.

        Returns:
            Optional[Player]: Winner player or None if game not over
        """
        return self._winner

    def ai_should_roll(self) -> bool:
        """Get AI decision for whether current player should roll.

        Uses the AI intelligence system to determine the best move
        based on current game state and difficulty level.

        Returns:
            bool: True if AI should roll, False if should hold

        Raises:
            RuntimeError: If current player is human
        """
        current_player = self.get_current_player()
        if current_player.is_human():
            raise RuntimeError("Current player is human")

        # Create game state for AI decision making
        game_state = self._create_game_state()
        return self._ai_intelligence.should_roll(game_state)

    def set_ai_difficulty(self, difficulty: DifficultyLevel) -> None:
        """Set the AI difficulty level.

        Args:
            difficulty (DifficultyLevel): New difficulty level
        """
        self._ai_intelligence.set_difficulty(difficulty)

    def get_ai_difficulty(self) -> DifficultyLevel:
        """Get current AI difficulty level.

        Returns:
            DifficultyLevel: Current AI difficulty
        """
        return self._ai_intelligence.get_difficulty()

    def _switch_player(self) -> None:
        """Switch to the other player's turn."""
        self._current_player_index = 1 - self._current_player_index

    def _create_game_state(self):
        """Create game state object for AI decision making.

        Returns:
            Object with methods needed by AI intelligence system
        """
        current_player = self.get_current_player()
        players = self.get_players()
        opponent = players[0] if current_player == players[1] else players[1]

        class GameState:
            """Simple game state for AI decision making."""

            def __init__(self, current, opponent, winning_score):
                self.current = current
                self.opponent = opponent
                self.winning = winning_score

            def get_current_player_total_score(self):
                return self.current.get_total_score()

            def get_current_player_turn_score(self):
                return self.current.get_turn_score()

            def get_opponent_score(self):
                return self.opponent.get_total_score()

            def get_winning_score(self):
                return self.winning

        return GameState(current_player, opponent, self._winning_score)

    def __str__(self) -> str:
        """String representation of the game.

        Returns:
            str: String describing the game matchup
        """
        return f"Game({self._player1.get_name()} vs {self._player2.get_name()})"
