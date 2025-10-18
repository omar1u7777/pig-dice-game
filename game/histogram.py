"""Histogram module for displaying dice roll statistics.

This module provides visualization of dice roll frequencies and statistics
in a text-based format suitable for terminal display.
"""

from typing import Dict, List
from collections import Counter


class Histogram:
    """Creates visual histogram of dice roll statistics.

    This class collects dice roll data and provides methods to display
    the frequency distribution in a user-friendly text format.

    Attributes:
        _rolls (List[int]): List of all recorded dice rolls
    """

    def __init__(self) -> None:
        """Initialize empty histogram."""
        self._rolls: List[int] = []

    def add_roll(self, value: int) -> None:
        """Add a dice roll to the statistics.

        Args:
            value (int): Dice roll value (must be positive)

        Raises:
            ValueError: If value is not positive
        """
        if value < 1:
            raise ValueError("Roll value must be positive")
        self._rolls.append(value)

    def add_rolls(self, values: List[int]) -> None:
        """Add multiple rolls at once.

        Args:
            values (List[int]): List of dice roll values
        """
        for value in values:
            self.add_roll(value)

    def get_counts(self) -> Dict[int, int]:
        """Get count of each roll value.

        Returns:
            Dict[int, int]: Dictionary mapping roll value to count
        """
        return dict(Counter(self._rolls))

    def get_total_rolls(self) -> int:
        """Get total number of rolls recorded.

        Returns:
            int: Total rolls recorded
        """
        return len(self._rolls)

    def get_percentage(self, value: int) -> float:
        """Get percentage for a specific dice value.

        Args:
            value (int): Dice value to check

        Returns:
            float: Percentage (0-100) of rolls that were this value
        """
        if not self._rolls:
            return 0.0
        count = self._rolls.count(value)
        return (count / len(self._rolls)) * 100

    def display(self) -> str:
        """Create visual histogram display.

        Returns:
            str: Multi-line string representation of histogram with bars
        """
        if not self._rolls:
            return "📊 No rolls recorded yet."

        counts = self.get_counts()
        total = len(self._rolls)

        result = ["📊 Dice Roll Statistics", "=" * 30]
        result.append(f"Total rolls: {total}")
        result.append("")

        # Show statistics for dice faces 1-6
        for face in range(1, 7):
            count = counts.get(face, 0)
            percentage = (count / total * 100) if total > 0 else 0

            # Create visual bar (scale down for terminal display)
            bar_length = int(percentage / 2)  # 50% = 25 chars max
            bar = "█" * bar_length

            result.append(f"{face}: {count:3d} ({percentage:5.1f}%) {bar}")

        return "\n".join(result)

    def clear(self) -> None:
        """Clear all recorded rolls."""
        self._rolls.clear()

    def get_most_common(self) -> int:
        """Get the most commonly rolled value.

        Returns:
            int: Most common roll value, or 0 if no rolls recorded
        """
        if not self._rolls:
            return 0
        return Counter(self._rolls).most_common(1)[0][0]

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: Simple description of histogram
        """
        return f"Histogram({len(self._rolls)} rolls)"
