"""Unit tests for the Dice class."""

import pytest
from unittest.mock import patch
from game.dice import Dice


class TestDice:
    """Test cases for the Dice class."""

    def test_init_default_sides(self):
        """Test initialization with default sides."""
        dice = Dice()
        assert dice.get_sides() == 6
        assert dice.get_history() == []

    def test_init_custom_sides(self):
        """Test initialization with custom sides."""
        dice = Dice(10)
        assert dice.get_sides() == 10

    def test_init_invalid_sides(self):
        """Test initialization with invalid sides raises ValueError."""
        with pytest.raises(ValueError, match="Dice must have at least 2 sides"):
            Dice(1)

    def test_roll_returns_valid_value(self):
        """Test that roll returns a value between 1 and sides."""
        dice = Dice(6)
        result = dice.roll()
        assert 1 <= result <= 6
        assert len(dice.get_history()) == 1

    def test_roll_adds_to_history(self):
        """Test that roll adds result to history."""
        dice = Dice()
        dice.roll()
        assert len(dice.get_history()) == 1

    def test_get_sides(self):
        """Test getting the number of sides."""
        dice = Dice(8)
        assert dice.get_sides() == 8

    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not the original list."""
        dice = Dice()
        dice.roll()
        history = dice.get_history()
        history.append(999)  # Modify the returned list
        assert 999 not in dice.get_history()  # Original should be unchanged

    def test_clear_history(self):
        """Test clearing the roll history."""
        dice = Dice()
        dice.roll()
        dice.roll()
        assert len(dice.get_history()) == 2
        dice.clear_history()
        assert len(dice.get_history()) == 0

    def test_get_last_roll_no_rolls(self):
        """Test get_last_roll raises IndexError when no rolls made."""
        dice = Dice()
        with pytest.raises(IndexError, match="No rolls have been made yet"):
            dice.get_last_roll()

    def test_get_last_roll_after_roll(self):
        """Test get_last_roll returns the last rolled value."""
        dice = Dice()
        dice.roll()
        last_roll = dice.get_last_roll()
        assert last_roll == dice.get_history()[-1]

    def test_str_no_rolls(self):
        """Test string representation when no rolls made."""
        dice = Dice()
        assert str(dice) == "🎲 Not rolled"

    def test_str_after_roll(self):
        """Test string representation after rolling."""
        dice = Dice()
        with patch("random.randint", return_value=4):
            dice.roll()
        assert str(dice) == "🎲 4"

    def test_repr(self):
        """Test detailed string representation."""
        dice = Dice(8)
        expected = "Dice(sides=8, history=[])"
        assert repr(dice) == expected

    def test_repr_with_history(self):
        """Test repr with roll history."""
        dice = Dice()
        with patch("random.randint", return_value=3):
            dice.roll()
        expected = "Dice(sides=6, history=[3])"
        assert repr(dice) == expected

    def test_multiple_rolls_history(self):
        """Test that multiple rolls are stored in history."""
        dice = Dice()
        with patch("random.randint", side_effect=[2, 5, 1]):
            dice.roll()
            dice.roll()
            dice.roll()
        history = dice.get_history()
        assert history == [2, 5, 1]

    def test_roll_range_custom_sides(self):
        """Test roll returns valid values for custom sided dice."""
        dice = Dice(12)
        with patch("random.randint", return_value=7):
            result = dice.roll()
        assert 1 <= result <= 12
        assert result == 7

    def test_clear_history_preserves_sides(self):
        """Test that clearing history doesn't affect sides."""
        dice = Dice(10)
        dice.roll()
        dice.clear_history()
        assert dice.get_sides() == 10
        assert len(dice.get_history()) == 0
