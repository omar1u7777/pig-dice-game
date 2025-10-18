"""DiceHand module for managing multiple dice in the Pig dice game.

This module contains the DiceHand class that manages one or more dice
and provides functionality for rolling multiple dice at once.
"""

from typing import List
from .dice import Dice


class DiceHand:
    """Manages a collection of dice for game play.

    This class represents a hand of dice that can be rolled together.
    It provides functionality to roll all dice, get individual results,
    and calculate totals.

    Attributes:
        _dice (List[Dice]): List of dice in this hand
        _last_roll (List[int]): Results of the last roll
    """

    def __init__(self, num_dice: int = 1, sides: int = 6) -> None:
        """Initialize a hand with the specified number of dice.

        Args:
            num_dice (int): Number of dice in the hand. Defaults to 1.
            sides (int): Number of sides on each die. Defaults to 6.

        Raises:
            ValueError: If num_dice is less than 1 or sides is less than 2.
        """
        if num_dice < 1:
            raise ValueError("Must have at least 1 die in hand")
        if sides < 2:
            raise ValueError("Dice must have at least 2 sides")

        self._dice: List[Dice] = [Dice(sides) for _ in range(num_dice)]
        self._last_roll: List[int] = []

    def roll(self) -> List[int]:
        """Roll all dice in the hand.

        Returns:
            List[int]: List of roll results, one for each die
        """
        self._last_roll = [die.roll() for die in self._dice]
        return self._last_roll.copy()

    def get_last_roll(self) -> List[int]:
        """Get the results of the last roll.

        Returns:
            List[int]: Copy of the last roll results

        Raises:
            RuntimeError: If no rolls have been made
        """
        if not self._last_roll:
            return []
        return self._last_roll.copy()

    def get_total(self) -> int:
        """Get the total sum of the last roll.

        Returns:
            int: Sum of all dice from the last roll
        """
        if not self._last_roll:
            return 0
        return sum(self._last_roll)

    def has_one(self) -> bool:
        """Check if any die in the last roll shows a 1.

        Returns:
            bool: True if any die shows 1, False otherwise
        """
        return 1 in self._last_roll

    def get_num_dice(self) -> int:
        """Get the number of dice in this hand.

        Returns:
            int: Number of dice
        """
        return len(self._dice)

    def get_dice_history(self, die_index: int) -> List[int]:
        """Get the roll history for a specific die.

        Args:
            die_index (int): Index of the die (0-based)

        Returns:
            List[int]: Copy of the specified die's roll history

        Raises:
            IndexError: If die_index is out of range
        """
        if die_index < 0 or die_index >= len(self._dice):
            raise IndexError(f"Die index {die_index} out of range")
        return self._dice[die_index].get_history()

    def clear_history(self) -> None:
        """Clear the roll history for all dice."""
        for die in self._dice:
            die.clear_history()
        self._last_roll.clear()

    def __str__(self) -> str:
        """String representation of the dice hand.

        Returns:
            str: Description of the hand and last roll
        """
        if self._last_roll:
            if len(self._last_roll) == 1:
                return f" {self._last_roll[0]}"
            roll_str = ", ".join(map(str, self._last_roll))
            return f" [{roll_str}]"
        return " Not rolled"

    def __repr__(self) -> str:
        """Detailed string representation.

        Returns:
            str: Detailed representation
        """
        return f"DiceHand(num_dice={len(self._dice)}, last_roll={self._last_roll})"
