"""Intelligence module for AI players in the Pig dice game.

This module contains different AI strategies for computer players
with varying levels of difficulty and risk assessment.
"""

import random
from enum import Enum
from typing import Protocol


class DifficultyLevel(Enum):
    """Enumeration of AI difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameStateProtocol(Protocol):
    """Protocol defining the game state interface for AI decision making."""

    def get_current_player_total_score(self) -> int:
        """Get current player's total score."""
        ...

    def get_current_player_turn_score(self) -> int:
        """Get current player's turn score."""
        ...

    def get_opponent_score(self) -> int:
        """Get opponent's total score."""
        ...

    def get_winning_score(self) -> int:
        """Get the score needed to win."""
        ...


class Intelligence:
    """AI intelligence for computer players.

    This class implements different strategies for AI decision making
    based on the current game state and difficulty level.

    Attributes:
        _difficulty (DifficultyLevel): Current difficulty level
        _risk_tolerance (float): Risk tolerance factor (0.0 to 1.0)
    """

    def __init__(self, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM) -> None:
        """Initialize AI intelligence with specified difficulty.

        Args:
            difficulty (DifficultyLevel): AI difficulty level
        """
        self._difficulty = difficulty
        self._risk_tolerance = self._calculate_risk_tolerance()

    def _calculate_risk_tolerance(self) -> float:
        """Calculate risk tolerance based on difficulty level.

        Returns:
            float: Risk tolerance value between 0.0 and 1.0
        """
        if self._difficulty == DifficultyLevel.EASY:
            return 0.2  # Very conservative
        elif self._difficulty == DifficultyLevel.MEDIUM:
            return 0.5  # Balanced
        else:  # HARD
            return 0.8  # Aggressive

    def should_roll(self, game_state: GameStateProtocol) -> bool:
        """Decide whether the AI should roll or hold.

        Args:
            game_state (GameStateProtocol): Current game state

        Returns:
            bool: True if AI should roll, False if should hold
        """
        if self._difficulty == DifficultyLevel.EASY:
            return self._easy_strategy(game_state)
        elif self._difficulty == DifficultyLevel.MEDIUM:
            return self._medium_strategy(game_state)
        else:  # HARD
            return self._hard_strategy(game_state)

    def _easy_strategy(self, game_state: GameStateProtocol) -> bool:
        """Conservative strategy for easy difficulty.

        Args:
            game_state (GameStateProtocol): Current game state

        Returns:
            bool: Decision to roll or hold
        """
        turn_score = game_state.get_current_player_turn_score()

        # Very conservative: hold at 15 points or more
        if turn_score >= 15:
            return False

        # Also consider if close to winning
        total_score = game_state.get_current_player_total_score()
        winning_score = game_state.get_winning_score()

        if total_score + turn_score >= winning_score:
            return False

        return True

    def _medium_strategy(self, game_state: GameStateProtocol) -> bool:
        """Balanced strategy for medium difficulty.

        Args:
            game_state (GameStateProtocol): Current game state

        Returns:
            bool: Decision to roll or hold
        """
        turn_score = game_state.get_current_player_turn_score()
        total_score = game_state.get_current_player_total_score()
        opponent_score = game_state.get_opponent_score()
        winning_score = game_state.get_winning_score()

        # Can win with current turn score
        if total_score + turn_score >= winning_score:
            return False

        # Opponent is close to winning, take more risks
        if opponent_score >= winning_score - 20:
            threshold = 25
        else:
            threshold = 20

        # Add some randomness to make it less predictable
        random_factor = random.randint(-3, 3)

        return turn_score < (threshold + random_factor)

    def _hard_strategy(self, game_state: GameStateProtocol) -> bool:
        """Aggressive and adaptive strategy for hard difficulty.

        Args:
            game_state (GameStateProtocol): Current game state

        Returns:
            bool: Decision to roll or hold
        """
        turn_score = game_state.get_current_player_turn_score()
        total_score = game_state.get_current_player_total_score()
        opponent_score = game_state.get_opponent_score()
        winning_score = game_state.get_winning_score()

        # Can win with current turn score
        if total_score + turn_score >= winning_score:
            return False

        # Calculate score difference
        score_diff = opponent_score - total_score

        # Adaptive threshold based on game situation
        base_threshold = 20

        # Behind in score: take more risks
        if score_diff > 20:
            threshold = base_threshold + 10
        elif score_diff > 0:
            threshold = base_threshold + 5
        # Ahead in score: be more conservative
        elif score_diff < -20:
            threshold = base_threshold - 5
        else:
            threshold = base_threshold

        # If opponent is very close to winning, be very aggressive
        if opponent_score >= winning_score - 15:
            threshold = max(30, threshold + 10)

        # Consider probability of busting
        # After rolling several times, probability of getting 1 increases
        if turn_score > 25:
            # Add probability consideration
            bust_risk = min(0.3, turn_score / 100)  # Approximate risk
            if random.random() < bust_risk:
                return False

        return turn_score < threshold

    def get_difficulty(self) -> DifficultyLevel:
        """Get the current difficulty level.

        Returns:
            DifficultyLevel: Current difficulty
        """
        return self._difficulty

    def set_difficulty(self, difficulty: DifficultyLevel) -> None:
        """Set the AI difficulty level.

        Args:
            difficulty (DifficultyLevel): New difficulty level
        """
        self._difficulty = difficulty
        self._risk_tolerance = self._calculate_risk_tolerance()

    def get_risk_tolerance(self) -> float:
        """Get the current risk tolerance.

        Returns:
            float: Risk tolerance value
        """
        return self._risk_tolerance

    def __str__(self) -> str:
        """String representation of the intelligence.

        Returns:
            str: Description of difficulty and risk tolerance
        """
        return (
            f"Intelligence({self._difficulty.value}, risk={self._risk_tolerance:.1f})"
        )

    def __repr__(self) -> str:
        """Detailed string representation.

        Returns:
            str: Detailed representation
        """
        return (
            f"Intelligence(difficulty={self._difficulty}, "
            f"risk_tolerance={self._risk_tolerance})"
        )
