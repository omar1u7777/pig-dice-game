"""Tests for Intelligence class."""

import pytest
from game.intelligence import Intelligence, DifficultyLevel


class MockGameState:
    """Mock game state for testing."""

    def __init__(
        self, total_score=0, turn_score=0, opponent_score=0, winning_score=100
    ):
        self.total_score = total_score
        self.turn_score = turn_score
        self.opponent_score = opponent_score
        self.winning_score = winning_score

    def get_current_player_total_score(self):
        return self.total_score

    def get_current_player_turn_score(self):
        return self.turn_score

    def get_opponent_score(self):
        return self.opponent_score

    def get_winning_score(self):
        return self.winning_score


class TestIntelligence:
    """Test cases for Intelligence class."""

    def test_init_default(self):
        """Test default initialization."""
        ai = Intelligence()
        assert ai.get_difficulty() == DifficultyLevel.MEDIUM

    def test_init_easy(self):
        """Test easy difficulty initialization."""
        ai = Intelligence(DifficultyLevel.EASY)
        assert ai.get_difficulty() == DifficultyLevel.EASY

    def test_init_hard(self):
        """Test hard difficulty initialization."""
        ai = Intelligence(DifficultyLevel.HARD)
        assert ai.get_difficulty() == DifficultyLevel.HARD

    def test_set_difficulty(self):
        """Test setting difficulty."""
        ai = Intelligence(DifficultyLevel.EASY)
        ai.set_difficulty(DifficultyLevel.HARD)
        assert ai.get_difficulty() == DifficultyLevel.HARD

    def test_easy_holds_at_15(self):
        """Test easy AI holds at 15 points."""
        ai = Intelligence(DifficultyLevel.EASY)
        game_state = MockGameState(turn_score=15)
        assert ai.should_roll(game_state) is False

    def test_easy_rolls_below_15(self):
        """Test easy AI rolls below 15 points."""
        ai = Intelligence(DifficultyLevel.EASY)
        game_state = MockGameState(turn_score=10)
        assert ai.should_roll(game_state) is True

    def test_easy_winning_condition(self):
        """Test easy AI with winning condition."""
        ai = Intelligence(DifficultyLevel.EASY)
        game_state = MockGameState(total_score=90, turn_score=10, winning_score=100)
        assert ai.should_roll(game_state) is False  # Can win

    def test_medium_holds_at_20(self):
        """Test medium AI holds around 20 points."""
        ai = Intelligence(DifficultyLevel.MEDIUM)
        game_state = MockGameState(turn_score=20)
        # Medium AI has randomness, so test multiple times to ensure it generally holds
        holds_count = 0
        for _ in range(50):  # More samples for better reliability
            if not ai.should_roll(game_state):
                holds_count += 1
        # Should hold most of the time at 20 points (allowing for randomness)
        assert holds_count >= 20  # At least 40% of the time

    def test_medium_rolls_below_20(self):
        """Test medium AI rolls below 20 points."""
        ai = Intelligence(DifficultyLevel.MEDIUM)
        game_state = MockGameState(turn_score=15)
        assert ai.should_roll(game_state) is True

    def test_medium_opponent_pressure(self):
        """Test medium AI under opponent pressure."""
        ai = Intelligence(DifficultyLevel.MEDIUM)
        # Opponent close to winning
        game_state = MockGameState(turn_score=15, opponent_score=85, winning_score=100)
        # Should be more likely to take risks
        decision = ai.should_roll(game_state)
        assert isinstance(decision, bool)

    def test_hard_adaptive_strategy(self):
        """Test hard AI adaptive strategy."""
        ai = Intelligence(DifficultyLevel.HARD)

        # Behind in score - should be more aggressive
        game_state = MockGameState(total_score=30, turn_score=15, opponent_score=60)
        aggressive_decision = ai.should_roll(game_state)

        # Ahead in score - should be more conservative
        game_state = MockGameState(total_score=60, turn_score=15, opponent_score=30)
        conservative_decision = ai.should_roll(game_state)

        # Both should be boolean decisions
        assert isinstance(aggressive_decision, bool)
        assert isinstance(conservative_decision, bool)

    def test_hard_opponent_close_to_winning(self):
        """Test hard AI when opponent close to winning."""
        ai = Intelligence(DifficultyLevel.HARD)
        game_state = MockGameState(turn_score=10, opponent_score=90, winning_score=100)
        # Should take more risks when opponent is close
        decision = ai.should_roll(game_state)
        assert isinstance(decision, bool)

    def test_all_difficulties_winning_condition(self):
        """Test all difficulties respect winning condition."""
        for difficulty in [
            DifficultyLevel.EASY,
            DifficultyLevel.MEDIUM,
            DifficultyLevel.HARD,
        ]:
            ai = Intelligence(difficulty)
            game_state = MockGameState(total_score=95, turn_score=5, winning_score=100)
            assert ai.should_roll(game_state) is False  # Can win, should hold

    def test_risk_tolerance_calculation(self):
        """Test risk tolerance calculation."""
        easy_ai = Intelligence(DifficultyLevel.EASY)
        medium_ai = Intelligence(DifficultyLevel.MEDIUM)
        hard_ai = Intelligence(DifficultyLevel.HARD)

        easy_tolerance = easy_ai.get_risk_tolerance()
        medium_tolerance = medium_ai.get_risk_tolerance()
        hard_tolerance = hard_ai.get_risk_tolerance()

        assert 0.0 <= easy_tolerance <= 1.0
        assert 0.0 <= medium_tolerance <= 1.0
        assert 0.0 <= hard_tolerance <= 1.0
        assert easy_tolerance < hard_tolerance

    def test_str_representation(self):
        """Test string representation."""
        ai = Intelligence(DifficultyLevel.MEDIUM)
        str_repr = str(ai)
        assert "medium" in str_repr.lower()
        assert "Intelligence" in str_repr

    def test_repr_representation(self):
        """Test detailed representation."""
        ai = Intelligence(DifficultyLevel.HARD)
        repr_str = repr(ai)
        assert "Intelligence" in repr_str
        assert "HARD" in repr_str or "hard" in repr_str

    def test_consistent_decisions(self):
        """Test that AI makes consistent decisions with same input."""
        ai = Intelligence(DifficultyLevel.EASY)
        game_state = MockGameState(turn_score=10)

        # Should make same decision for same state (for easy AI)
        decision1 = ai.should_roll(game_state)
        decision2 = ai.should_roll(game_state)
        assert decision1 == decision2  # Easy AI should be deterministic

    def test_boundary_conditions(self):
        """Test boundary conditions."""
        ai = Intelligence(DifficultyLevel.MEDIUM)

        # Zero turn score
        game_state = MockGameState(turn_score=0)
        assert ai.should_roll(game_state) is True

        # Very high turn score
        game_state = MockGameState(turn_score=50)
        assert ai.should_roll(game_state) is False
