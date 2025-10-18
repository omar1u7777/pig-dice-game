"""Player module for the Pig dice game.

This module contains the Player class that represents a player
in the game with name, score, and game statistics.
"""

import uuid
from typing import Optional


class Player:
    """Represents a player in the Pig dice game.

    This class manages player information including name, current score,
    turn score, and a unique identifier that persists across name changes.

    Attributes:
        _player_id (str): Unique identifier for the player
        _name (str): Player's display name
        _total_score (int): Player's total accumulated score
        _turn_score (int): Player's current turn score
        _is_human (bool): Whether this is a human or AI player
    """

    def __init__(
        self, name: str, is_human: bool = True, player_id: Optional[str] = None
    ) -> None:
        """Initialize a new player.

        Args:
            name (str): Player's name
            is_human (bool): Whether this is a human player. Defaults to True.
            player_id (Optional[str]): Unique ID for the player. Generated if None.

        Raises:
            ValueError: If name is empty or only whitespace.
        """
        if not name or not name.strip():
            raise ValueError("Player name cannot be empty")

        self._player_id = player_id or str(uuid.uuid4())
        self._name = name.strip()
        self._total_score = 0
        self._turn_score = 0
        self._is_human = is_human

    def get_id(self) -> str:
        """Get the player's unique ID.

        Returns:
            str: Player's unique identifier
        """
        return self._player_id

    def get_name(self) -> str:
        """Get the player's name.

        Returns:
            str: Player's current name
        """
        return self._name

    def set_name(self, name: str) -> None:
        """Set the player's name.

        Args:
            name (str): New name for the player

        Raises:
            ValueError: If name is empty or only whitespace.
        """
        if not name or not name.strip():
            raise ValueError("Player name cannot be empty")
        self._name = name.strip()

    def get_total_score(self) -> int:
        """Get the player's total score.

        Returns:
            int: Total accumulated score
        """
        return self._total_score

    def get_turn_score(self) -> int:
        """Get the player's current turn score.

        Returns:
            int: Current turn score
        """
        return self._turn_score

    def add_to_turn(self, points: int) -> None:
        """Add points to the current turn score.

        Args:
            points (int): Points to add to turn score

        Raises:
            ValueError: If points is negative.
        """
        if points < 0:
            raise ValueError("Cannot add negative points")
        self._turn_score += points

    def hold_turn(self) -> int:
        """Bank the current turn score and add it to total score.

        Returns:
            int: The points that were banked
        """
        banked_points = self._turn_score
        self._total_score += self._turn_score
        self._turn_score = 0
        return banked_points

    def lose_turn(self) -> int:
        """Lose the current turn and reset turn score to 0.

        Returns:
            int: The points that were lost
        """
        lost_points = self._turn_score
        self._turn_score = 0
        return lost_points

    def reset_scores(self) -> None:
        """Reset both total and turn scores to 0."""
        self._total_score = 0
        self._turn_score = 0

    def is_human(self) -> bool:
        """Check if this is a human player.

        Returns:
            bool: True if human player, False if AI
        """
        return self._is_human

    def has_won(self, winning_score: int = 100) -> bool:
        """Check if the player has won the game.

        Args:
            winning_score (int): Score needed to win. Defaults to 100.

        Returns:
            bool: True if total score >= winning_score
        """
        return self._total_score >= winning_score

    def get_combined_score(self) -> int:
        """Get the combined total and turn score.

        Returns:
            int: Total score + turn score
        """
        return self._total_score + self._turn_score

    def __str__(self) -> str:
        """String representation of the player.

        Returns:
            str: Player description with name and scores
        """
        symbol = "👤" if self._is_human else "🤖"
        return f"{symbol} {self._name}: {self._total_score} + {self._turn_score}"

    def __repr__(self) -> str:
        """Detailed string representation.

        Returns:
            str: Detailed representation
        """
        return (
            f"Player(id='{self._player_id}', name='{self._name}', "
            f"total={self._total_score}, turn={self._turn_score}, "
            f"human={self._is_human})"
        )

    def __eq__(self, other) -> bool:
        """Check equality based on player ID.

        Args:
            other: Another object to compare with

        Returns:
            bool: True if same player ID
        """
        if not isinstance(other, Player):
            return False
        return self._player_id == other._player_id
