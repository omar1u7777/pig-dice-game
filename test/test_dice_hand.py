"""Tests for DiceHand class."""

import pytest
from game.dice_hand import DiceHand


class TestDiceHand:
    """Test cases for DiceHand class."""

    def test_init_default(self):
        """Test default initialization."""
        hand = DiceHand()
        assert hand.get_num_dice() == 1
        assert hand.get_last_roll() == []

    def test_init_multiple_dice(self):
        """Test initialization with multiple dice."""
        hand = DiceHand(3)
        assert hand.get_num_dice() == 3

    def test_init_invalid_dice_count(self):
        """Test initialization with invalid dice count."""
        with pytest.raises(ValueError):
            DiceHand(0)
        with pytest.raises(ValueError):
            DiceHand(-1)

    def test_roll_single_die(self):
        """Test rolling single die."""
        hand = DiceHand(1)
        results = hand.roll()
        assert len(results) == 1
        assert 1 <= results[0] <= 6
        assert hand.get_last_roll() == results

    def test_roll_multiple_dice(self):
        """Test rolling multiple dice."""
        hand = DiceHand(3)
        results = hand.roll()
        assert len(results) == 3
        for result in results:
            assert 1 <= result <= 6

    def test_get_total_single_die(self):
        """Test getting total for single die."""
        hand = DiceHand(1)
        hand.roll()
        total = hand.get_total()
        assert 1 <= total <= 6
        assert total == hand.get_last_roll()[0]

    def test_get_total_multiple_dice(self):
        """Test getting total for multiple dice."""
        hand = DiceHand(2)
        results = hand.roll()
        total = hand.get_total()
        assert total == sum(results)
        assert 2 <= total <= 12

    def test_get_total_no_roll(self):
        """Test getting total when no roll made."""
        hand = DiceHand()
        assert hand.get_total() == 0

    def test_has_one_true(self):
        """Test has_one when there is a 1."""
        hand = DiceHand(1)
        # Keep rolling until we get a 1 (for test purposes)
        for _ in range(100):  # Safety limit
            hand.roll()
            if 1 in hand.get_last_roll():
                assert hand.has_one() is True
                break
        else:
            # If we somehow don't get a 1 in 100 rolls, manually set it
            hand._last_roll = [1]
            assert hand.has_one() is True

    def test_has_one_false(self):
        """Test has_one when there is no 1."""
        hand = DiceHand(1)
        # Manually set roll to not include 1
        hand._last_roll = [6]
        assert hand.has_one() is False

    def test_has_one_multiple_dice(self):
        """Test has_one with multiple dice."""
        hand = DiceHand(3)
        hand._last_roll = [2, 1, 5]
        assert hand.has_one() is True

        hand._last_roll = [2, 3, 5]
        assert hand.has_one() is False

    def test_get_last_roll_copy(self):
        """Test that get_last_roll returns a copy."""
        hand = DiceHand(1)
        hand.roll()
        roll1 = hand.get_last_roll()
        roll2 = hand.get_last_roll()
        assert roll1 == roll2
        assert roll1 is not roll2  # Different objects

    def test_multiple_rolls(self):
        """Test multiple consecutive rolls."""
        hand = DiceHand(1)
        results1 = hand.roll()
        results2 = hand.roll()

        # Last roll should be the most recent
        assert hand.get_last_roll() == results2
        assert hand.get_last_roll() != results1 or results1 == results2

    def test_str_representation_not_rolled(self):
        """Test string representation when not rolled."""
        hand = DiceHand()
        str_repr = str(hand)
        assert "Not rolled" in str_repr
        assert "" in str_repr

    def test_str_representation_rolled(self):
        """Test string representation after rolling."""
        hand = DiceHand(1)
        hand.roll()
        str_repr = str(hand)
        assert "" in str_repr
        # Should contain the rolled number
        assert str(hand.get_last_roll()[0]) in str_repr or "" in str_repr

    def test_dice_hand_consistency(self):
        """Test that dice hand maintains consistency."""
        hand = DiceHand(2)

        for _ in range(10):
            results = hand.roll()
            assert len(results) == 2
            assert hand.get_num_dice() == 2
            assert hand.get_last_roll() == results
            assert hand.get_total() == sum(results)

    def test_large_dice_count(self):
        """Test with larger number of dice."""
        hand = DiceHand(10)
        results = hand.roll()
        assert len(results) == 10
        assert hand.get_num_dice() == 10
        assert 10 <= hand.get_total() <= 60
        assert all(1 <= result <= 6 for result in results)

    def test_edge_case_operations(self):
        """Test edge case operations."""
        hand = DiceHand(1)

        # Test before any roll
        assert hand.get_total() == 0
        assert hand.get_last_roll() == []

        # Test after roll
        hand.roll()
        assert len(hand.get_last_roll()) == 1
        assert hand.get_total() > 0

    def test_init_custom_sides(self):
        """Test initialization with custom number of sides."""
        hand = DiceHand(1, 10)
        assert hand.get_num_dice() == 1
        hand.roll()
        result = hand.get_last_roll()[0]
        assert 1 <= result <= 10

    def test_init_invalid_sides(self):
        """Test initialization with invalid number of sides."""
        with pytest.raises(ValueError):
            DiceHand(1, 1)
        with pytest.raises(ValueError):
            DiceHand(1, 0)

    def test_get_dice_history_valid_index(self):
        """Test getting dice history for valid index."""
        hand = DiceHand(2)
        hand.roll()
        history = hand.get_dice_history(0)
        assert isinstance(history, list)
        assert len(history) >= 1  # At least one roll

    def test_get_dice_history_invalid_index(self):
        """Test getting dice history for invalid index."""
        hand = DiceHand(2)
        with pytest.raises(IndexError):
            hand.get_dice_history(-1)
        with pytest.raises(IndexError):
            hand.get_dice_history(2)

    def test_clear_history(self):
        """Test clearing roll history."""
        hand = DiceHand(2)
        hand.roll()
        assert len(hand.get_last_roll()) == 2
        assert hand.get_total() > 0

        hand.clear_history()
        assert hand.get_last_roll() == []
        assert hand.get_total() == 0

    def test_str_multiple_dice(self):
        """Test string representation with multiple dice."""
        hand = DiceHand(3)
        hand._last_roll = [2, 4, 6]
        str_repr = str(hand)
        assert "" in str_repr
        assert "[2, 4, 6]" in str_repr

    def test_repr(self):
        """Test detailed string representation."""
        hand = DiceHand(2)
        repr_str = repr(hand)
        assert "DiceHand" in repr_str
        assert "num_dice=2" in repr_str
        assert "last_roll=[]" in repr_str

        hand.roll()
        repr_str = repr(hand)
        assert "last_roll=" in repr_str
        assert len(hand.get_last_roll()) == 2
