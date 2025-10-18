"""Tests for Game class."""

import pytest
from unittest.mock import Mock, patch
from game.game import Game
from game.player import Player
from game.intelligence import DifficultyLevel


class TestGame:
    """Test cases for Game class."""

    def setup_method(self):
        """Set up test with two players."""
        self.player1 = Player("Alice", is_human=True)
        self.player2 = Player("Bob", is_human=False)
        self.game = Game(self.player1, self.player2)

    def test_init_game(self):
        """Test game initialization."""
        assert self.game.get_players() == (self.player1, self.player2)
        assert self.game.get_winning_score() == 100
        assert self.game.is_game_over() is False
        assert self.game.get_winner() is None

    def test_init_custom_winning_score(self):
        """Test initialization with custom winning score."""
        game = Game(self.player1, self.player2, winning_score=50)
        assert game.get_winning_score() == 50

    def test_start_game(self):
        """Test starting the game."""
        # Add some scores first
        self.player1.add_to_turn(10)
        self.player1.hold_turn()

        self.game.start_game()

        # Scores should be reset
        assert self.player1.get_total_score() == 0
        assert self.player1.get_turn_score() == 0
        assert self.player2.get_total_score() == 0
        assert self.player2.get_turn_score() == 0
        assert self.game.is_game_over() is False

    def test_get_current_player_initial(self):
        """Test getting current player initially."""
        assert self.game.get_current_player() == self.player1

    def test_roll_dice_before_start(self):
        """Test rolling dice before game starts."""
        with pytest.raises(RuntimeError, match="Game not started"):
            self.game.roll_dice()

    def test_roll_dice_normal(self):
        """Test normal dice roll."""
        self.game.start_game()

        with patch.object(self.game._dice_hand, "roll", return_value=[4]):
            result = self.game.roll_dice()
            assert result == 4
            assert self.player1.get_turn_score() == 4
            assert self.game.get_current_player() == self.player1  # Still same player

    def test_roll_dice_busts(self):
        """Test dice roll that busts (rolls 1)."""
        self.game.start_game()
        self.player1.add_to_turn(15)  # Add some points first

        with patch.object(self.game._dice_hand, "roll", return_value=[1]):
            result = self.game.roll_dice()
            assert result == 1
            assert self.player1.get_turn_score() == 0  # Lost turn points
            assert self.game.get_current_player() == self.player2  # Switched player

    def test_hold_turn_before_start(self):
        """Test holding turn before game starts."""
        with pytest.raises(RuntimeError, match="Game not started"):
            self.game.hold_turn()

    def test_hold_turn_normal(self):
        """Test normal hold turn."""
        self.game.start_game()
        self.player1.add_to_turn(20)

        banked = self.game.hold_turn()
        assert banked == 20
        assert self.player1.get_total_score() == 20
        assert self.player1.get_turn_score() == 0
        assert self.game.get_current_player() == self.player2  # Switched

    def test_hold_turn_wins_game(self):
        """Test holding turn that wins the game."""
        self.game.start_game()
        self.player1._total_score = 90  # Close to winning
        self.player1.add_to_turn(15)

        banked = self.game.hold_turn()
        assert banked == 15
        assert self.player1.get_total_score() == 105
        assert self.game.is_game_over() is True
        assert self.game.get_winner() == self.player1

    def test_ai_should_roll_human_player(self):
        """Test AI decision when current player is human."""
        self.game.start_game()
        # Current player is human (player1)
        with pytest.raises(RuntimeError, match="Current player is human"):
            self.game.ai_should_roll()

    def test_ai_should_roll_ai_player(self):
        """Test AI decision for AI player."""
        self.game.start_game()
        # Switch to AI player (player2)
        self.game._current_player_index = 1

        decision = self.game.ai_should_roll()
        assert isinstance(decision, bool)

    def test_set_ai_difficulty(self):
        """Test setting AI difficulty."""
        self.game.set_ai_difficulty(DifficultyLevel.HARD)
        assert self.game.get_ai_difficulty() == DifficultyLevel.HARD

        self.game.set_ai_difficulty(DifficultyLevel.EASY)
        assert self.game.get_ai_difficulty() == DifficultyLevel.EASY

    def test_game_over_operations(self):
        """Test operations when game is over."""
        self.game.start_game()
        self.game._game_over = True

        with pytest.raises(RuntimeError, match="Game is over"):
            self.game.roll_dice()

        with pytest.raises(RuntimeError, match="Game is over"):
            self.game.hold_turn()

    def test_player_switching(self):
        """Test player switching mechanism."""
        self.game.start_game()
        assert self.game.get_current_player() == self.player1

        # Force switch (simulate bust)
        self.game._switch_player()
        assert self.game.get_current_player() == self.player2

        self.game._switch_player()
        assert self.game.get_current_player() == self.player1

    def test_multiple_turns_same_player(self):
        """Test multiple rolls in same turn."""
        self.game.start_game()

        # Multiple successful rolls
        with patch.object(self.game._dice_hand, "roll", return_value=[3]):
            self.game.roll_dice()  # +3
            self.game.roll_dice()  # +3
            self.game.roll_dice()  # +3

        assert self.player1.get_turn_score() == 9
        assert self.game.get_current_player() == self.player1  # Same player

    def test_str_representation(self):
        """Test string representation."""
        str_repr = str(self.game)
        assert "Alice" in str_repr
        assert "Bob" in str_repr
        assert "Game" in str_repr

    def test_complete_game_simulation(self):
        """Test a complete game simulation."""
        self.game.start_game()

        # Simulate player 1 winning
        with patch.object(self.game._dice_hand, "roll", return_value=[5]):
            # Player 1 builds up score
            for _ in range(4):  # Roll 4 times = 20 points
                self.game.roll_dice()
            self.game.hold_turn()  # Bank 20 points

            # Player 2's turn (skip by forcing bust)
            with patch.object(self.game._dice_hand, "roll", return_value=[1]):
                self.game.roll_dice()  # Busts immediately

            # Player 1 continues and wins
            for _ in range(16):  # Need 80 more points
                self.game.roll_dice()
            self.game.hold_turn()  # Should win with 100+ points

        assert self.game.is_game_over()
        assert self.game.get_winner() == self.player1

    def test_game_state_for_ai(self):
        """Test game state creation for AI."""
        self.game.start_game()
        self.player1._total_score = 30
        self.player1.add_to_turn(10)
        self.player2._total_score = 45

        # Switch to AI player
        self.game._switch_player()
        self.player2.add_to_turn(5)

        game_state = self.game._create_game_state()

        assert game_state.get_current_player_total_score() == 45
        assert game_state.get_current_player_turn_score() == 5
        assert game_state.get_opponent_score() == 30
        assert game_state.get_winning_score() == 100

    def test_edge_case_exact_winning_score(self):
        """Test winning with exact winning score."""
        self.game.start_game()
        self.player1._total_score = 95
        self.player1.add_to_turn(5)  # Exactly 100

        self.game.hold_turn()

        assert self.player1.get_total_score() == 100
        assert self.game.is_game_over()
        assert self.game.get_winner() == self.player1
