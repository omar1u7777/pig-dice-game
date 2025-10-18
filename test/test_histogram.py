"""Tests for Histogram class."""

import pytest
from game.histogram import Histogram


class TestHistogram:
    """Test cases for Histogram class."""

    def test_init_empty(self):
        """Test initialization of empty histogram."""
        hist = Histogram()
        assert hist.get_total_rolls() == 0
        assert hist.get_counts() == {}
        assert str(hist) == "Histogram(0 rolls)"

    def test_add_single_roll(self):
        """Test adding a single roll."""
        hist = Histogram()
        hist.add_roll(3)
        assert hist.get_total_rolls() == 1
        assert hist.get_counts() == {3: 1}

    def test_add_multiple_rolls_same_value(self):
        """Test adding multiple rolls of same value."""
        hist = Histogram()
        hist.add_roll(4)
        hist.add_roll(4)
        hist.add_roll(4)
        assert hist.get_total_rolls() == 3
        assert hist.get_counts() == {4: 3}

    def test_add_multiple_rolls_different_values(self):
        """Test adding multiple rolls of different values."""
        hist = Histogram()
        hist.add_roll(1)
        hist.add_roll(3)
        hist.add_roll(6)
        hist.add_roll(3)

        counts = hist.get_counts()
        assert hist.get_total_rolls() == 4
        assert counts[1] == 1
        assert counts[3] == 2
        assert counts[6] == 1

    def test_add_invalid_roll(self):
        """Test adding invalid roll value."""
        hist = Histogram()
        with pytest.raises(ValueError):
            hist.add_roll(0)
        with pytest.raises(ValueError):
            hist.add_roll(-1)

    def test_add_rolls_list(self):
        """Test adding multiple rolls at once."""
        hist = Histogram()
        rolls = [1, 2, 3, 2, 1, 1]
        hist.add_rolls(rolls)

        assert hist.get_total_rolls() == 6
        counts = hist.get_counts()
        assert counts[1] == 3
        assert counts[2] == 2
        assert counts[3] == 1

    def test_get_percentage_single_value(self):
        """Test getting percentage for single value."""
        hist = Histogram()
        hist.add_rolls([2, 2, 2, 2, 6])  # 4 twos out of 5 rolls

        assert hist.get_percentage(2) == 80.0
        assert hist.get_percentage(6) == 20.0
        assert hist.get_percentage(1) == 0.0  # Not rolled

    def test_get_percentage_empty_histogram(self):
        """Test getting percentage from empty histogram."""
        hist = Histogram()
        assert hist.get_percentage(1) == 0.0
        assert hist.get_percentage(6) == 0.0

    def test_display_empty(self):
        """Test display of empty histogram."""
        hist = Histogram()
        display = hist.display()
        assert "No rolls recorded" in display
        assert "" in display

    def test_display_with_data(self):
        """Test display with data."""
        hist = Histogram()
        hist.add_rolls([1, 1, 2, 3, 3, 3, 6])

        display = hist.display()
        assert "" in display
        assert "Total rolls: 7" in display
        assert "1:" in display
        assert "3:" in display
        assert "█" in display  # Should have some bars

    def test_clear(self):
        """Test clearing histogram."""
        hist = Histogram()
        hist.add_rolls([1, 2, 3, 4, 5, 6])

        assert hist.get_total_rolls() == 6
        hist.clear()
        assert hist.get_total_rolls() == 0
        assert hist.get_counts() == {}

    def test_get_most_common_empty(self):
        """Test getting most common value from empty histogram."""
        hist = Histogram()
        assert hist.get_most_common() == 0

    def test_get_most_common_single(self):
        """Test getting most common value with single type."""
        hist = Histogram()
        hist.add_rolls([4, 4, 4])
        assert hist.get_most_common() == 4

    def test_get_most_common_multiple(self):
        """Test getting most common value with multiple types."""
        hist = Histogram()
        hist.add_rolls([1, 2, 2, 3, 3, 3, 3])
        assert hist.get_most_common() == 3  # Appears 4 times

    def test_percentage_calculation_precision(self):
        """Test percentage calculation precision."""
        hist = Histogram()
        hist.add_rolls([1, 2, 3])  # 1 out of 3 = 33.33...%

        percentage = hist.get_percentage(1)
        assert abs(percentage - 33.333333333333336) < 0.01

    def test_display_all_faces(self):
        """Test that display shows all dice faces 1-6."""
        hist = Histogram()
        hist.add_rolls([1, 2, 3, 4, 5, 6])

        display = hist.display()
        for face in range(1, 7):
            assert f"{face}:" in display

    def test_large_dataset(self):
        """Test with large dataset."""
        hist = Histogram()
        large_dataset = [i % 6 + 1 for i in range(1000)]  # 1000 rolls
        hist.add_rolls(large_dataset)

        assert hist.get_total_rolls() == 1000
        # Each face should appear roughly equally
        for face in range(1, 7):
            percentage = hist.get_percentage(face)
            assert 10 <= percentage <= 25  # Should be around 16.67%

    def test_str_representation_with_data(self):
        """Test string representation with data."""
        hist = Histogram()
        hist.add_rolls([1, 2, 3])
        str_repr = str(hist)
        assert "Histogram(3 rolls)" == str_repr

    def test_counts_immutability(self):
        """Test that get_counts returns independent copy."""
        hist = Histogram()
        hist.add_roll(1)

        counts1 = hist.get_counts()
        counts2 = hist.get_counts()

        counts1[1] = 999  # Modify one copy
        assert hist.get_counts()[1] == 1  # Original unchanged
        assert counts2[1] == 1  # Other copy unchanged
