"""Dice module for the Pig dice game.

This module contains the Dice class that represents a single die
with the ability to roll and return random values between 1 and 6.
"""

import random
from typing import List


class Dice:
    """Represents a single six-sided die.

    This class provides functionality to roll a die and get random
    values between 1 and 6. It also maintains a history of all rolls
    for statistical purposes.

    Attributes:
        _sides (int): Number of sides on the die (default: 6)
        _history (List[int]): History of all rolls made with this die
    """

    def __init__(self, sides: int = 6) -> None:
        """Initialize a new dice with specified number of sides.

        Args:
            sides (int): Number of sides on the die. Defaults to 6.

        Raises:
            ValueError: If sides is less than 2.
        """
        if sides < 2:
            raise ValueError("Dice must have at least 2 sides")
        self._sides = sides
        self._history: List[int] = []

    def roll(self) -> int:
        """Roll the die and return a random value.

        Returns:
            int: Random value between 1 and the number of sides (inclusive)
        """
        result = random.randint(1, self._sides)
        self._history.append(result)
        return result

    def get_sides(self) -> int:
        """Get the number of sides on this die.

        Returns:
            int: Number of sides
        """
        return self._sides

    def get_history(self) -> List[int]:
        """Get the history of all rolls made with this die.

        Returns:
            List[int]: Copy of the roll history
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear the roll history."""
        self._history.clear()

    def get_last_roll(self) -> int:
        """Get the last roll value.

        Returns:
            int: Last rolled value

        Raises:
            IndexError: If no rolls have been made
        """
        if not self._history:
            raise IndexError("No rolls have been made yet")
        return self._history[-1]

    def __str__(self) -> str:
        """String representation of the dice.

        Returns:
            str: Description of the dice
        """
        last_roll = self._history[-1] if self._history else "Not rolled"
        return f" {last_roll}"

    def __repr__(self) -> str:
        """Detailed string representation.

        Returns:
            str: Detailed representation including history
        """
        return f"Dice(sides={self._sides}, history={self._history})"
