"""Unit tests for the Player class."""

import pytest
from game.player import Player


class TestPlayer:
    """Test cases for the Player class."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        player = Player("Alice")
        assert player.get_name() == "Alice"
        assert player.is_human() is True
        assert player.get_total_score() == 0
        assert player.get_turn_score() == 0
        assert player.get_id() is not None

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        player = Player("Bob", is_human=False)
        assert player.get_name() == "Bob"
        assert player.is_human() is False

    def test_init_with_player_id(self):
        """Test initialization with custom player ID."""
        custom_id = "test-id-123"
        player = Player("Charlie", player_id=custom_id)
        assert player.get_id() == custom_id

    def test_init_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            Player("")

    def test_init_whitespace_name_raises_error(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            Player("   ")

    def test_init_name_stripped(self):
        """Test that name is stripped of whitespace."""
        player = Player("  Alice  ")
        assert player.get_name() == "Alice"

    def test_get_id_returns_string(self):
        """Test that get_id returns a string."""
        player = Player("Test")
        assert isinstance(player.get_id(), str)
        assert len(player.get_id()) > 0

    def test_get_name(self):
        """Test getting player name."""
        player = Player("Dave")
        assert player.get_name() == "Dave"

    def test_set_name_valid(self):
        """Test setting a valid new name."""
        player = Player("OldName")
        player.set_name("NewName")
        assert player.get_name() == "NewName"

    def test_set_name_stripped(self):
        """Test that set_name strips whitespace."""
        player = Player("Test")
        player.set_name("  New Name  ")
        assert player.get_name() == "New Name"

    def test_set_name_empty_raises_error(self):
        """Test that setting empty name raises ValueError."""
        player = Player("Test")
        with pytest.raises(ValueError, match="Player name cannot be empty"):
            player.set_name("")

    def test_get_total_score_initial(self):
        """Test initial total score is 0."""
        player = Player("Test")
        assert player.get_total_score() == 0

    def test_get_turn_score_initial(self):
        """Test initial turn score is 0."""
        player = Player("Test")
        assert player.get_turn_score() == 0

    def test_add_to_turn_positive(self):
        """Test adding positive points to turn score."""
        player = Player("Test")
        player.add_to_turn(5)
        assert player.get_turn_score() == 5

    def test_add_to_turn_multiple(self):
        """Test adding multiple values to turn score."""
        player = Player("Test")
        player.add_to_turn(3)
        player.add_to_turn(7)
        assert player.get_turn_score() == 10

    def test_add_to_turn_zero(self):
        """Test adding zero points."""
        player = Player("Test")
        player.add_to_turn(0)
        assert player.get_turn_score() == 0

    def test_add_to_turn_negative_raises_error(self):
        """Test that adding negative points raises ValueError."""
        player = Player("Test")
        with pytest.raises(ValueError, match="Cannot add negative points"):
            player.add_to_turn(-1)

    def test_hold_turn_banks_points(self):
        """Test that hold_turn adds turn score to total and resets turn."""
        player = Player("Test")
        player.add_to_turn(15)
        banked = player.hold_turn()
        assert banked == 15
        assert player.get_total_score() == 15
        assert player.get_turn_score() == 0

    def test_hold_turn_empty_turn(self):
        """Test holding with zero turn score."""
        player = Player("Test")
        banked = player.hold_turn()
        assert banked == 0
        assert player.get_total_score() == 0

    def test_lose_turn_resets_turn_score(self):
        """Test that lose_turn resets turn score and returns lost points."""
        player = Player("Test")
        player.add_to_turn(10)
        lost = player.lose_turn()
        assert lost == 10
        assert player.get_turn_score() == 0
        assert player.get_total_score() == 0

    def test_reset_scores(self):
        """Test resetting both scores."""
        player = Player("Test")
        player.add_to_turn(5)
        player.hold_turn()
        player.add_to_turn(3)
        player.reset_scores()
        assert player.get_total_score() == 0
        assert player.get_turn_score() == 0

    def test_is_human_default(self):
        """Test default human status."""
        player = Player("Test")
        assert player.is_human() is True

    def test_is_human_ai(self):
        """Test AI player status."""
        player = Player("AI", is_human=False)
        assert player.is_human() is False

    def test_has_won_default_threshold(self):
        """Test winning with default threshold."""
        player = Player("Test")
        assert not player.has_won()
        # Simulate winning score
        player._total_score = 100
        assert player.has_won()

    def test_has_won_custom_threshold(self):
        """Test winning with custom threshold."""
        player = Player("Test")
        player._total_score = 50
        assert not player.has_won(100)
        assert player.has_won(40)

    def test_get_combined_score(self):
        """Test getting combined score."""
        player = Player("Test")
        player._total_score = 20
        player.add_to_turn(5)
        assert player.get_combined_score() == 25

    def test_str_human_player(self):
        """Test string representation for human player."""
        player = Player("Alice", is_human=True)
        player._total_score = 25
        player.add_to_turn(10)
        expected = "👤 Alice: 25 + 10"
        assert str(player) == expected

    def test_str_ai_player(self):
        """Test string representation for AI player."""
        player = Player("Bot", is_human=False)
        player._total_score = 30
        player.add_to_turn(5)
        expected = "🤖 Bot: 30 + 5"
        assert str(player) == expected

    def test_repr(self):
        """Test detailed string representation."""
        player = Player("Test", is_human=False, player_id="test-id")
        player._total_score = 15
        player.add_to_turn(3)
        repr_str = repr(player)
        assert "Player(id='test-id'" in repr_str
        assert "name='Test'" in repr_str
        assert "total=15" in repr_str
        assert "turn=3" in repr_str
        assert "human=False" in repr_str

    def test_eq_same_id(self):
        """Test equality with same player ID."""
        id = "same-id"
        player1 = Player("Alice", player_id=id)
        player2 = Player("Bob", player_id=id)
        assert player1 == player2

    def test_eq_different_id(self):
        """Test inequality with different player IDs."""
        player1 = Player("Alice")
        player2 = Player("Alice")
        assert player1 != player2

    def test_eq_different_type(self):
        """Test inequality with different object types."""
        player = Player("Test")
        assert player != "not a player"
        assert player != 42

    def test_player_id_persistence_across_name_changes(self):
        """Test that player ID remains the same when name changes."""
        player = Player("Original")
        original_id = player.get_id()
        player.set_name("Changed")
        assert player.get_id() == original_id
        assert player.get_name() == "Changed"
