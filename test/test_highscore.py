"""Tests for HighScore class."""

import pytest
import os
import json
import tempfile
from game.highscore import HighScore


class TestHighScore:
    """Test cases for HighScore class."""

    def setup_method(self):
        """Set up test with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.filename = self.temp_file.name
        self.highscore = HighScore(self.filename)

    def teardown_method(self):
        """Clean up temporary file."""
        if os.path.exists(self.filename):
            os.unlink(self.filename)

    def test_init_new_file(self):
        """Test initialization with new file."""
        assert len(self.highscore.get_all_scores()) == 0
        assert str(self.highscore) == "HighScore(0 players)"

    def test_add_game_result_new_player(self):
        """Test adding game result for new player."""
        self.highscore.add_game_result("player1", "Alice", 75, True)

        stats = self.highscore.get_player_stats("player1")
        assert stats["name"] == "Alice"
        assert stats["games_played"] == 1
        assert stats["games_won"] == 1
        assert stats["total_points"] == 75
        assert stats["best_score"] == 75

    def test_add_game_result_existing_player(self):
        """Test adding game result for existing player."""
        # First game
        self.highscore.add_game_result("player1", "Alice", 75, True)
        # Second game
        self.highscore.add_game_result("player1", "Alice", 50, False)

        stats = self.highscore.get_player_stats("player1")
        assert stats["games_played"] == 2
        assert stats["games_won"] == 1
        assert stats["total_points"] == 125
        assert stats["best_score"] == 75

    def test_name_update_persistence(self):
        """Test that name updates but stats persist."""
        self.highscore.add_game_result("player1", "Alice", 75, True)
        self.highscore.add_game_result("player1", "Alicia", 60, False)

        stats = self.highscore.get_player_stats("player1")
        assert stats["name"] == "Alicia"  # Name updated
        assert stats["games_played"] == 2  # Stats persisted
        assert stats["total_points"] == 135

    def test_best_score_tracking(self):
        """Test best score tracking."""
        self.highscore.add_game_result("player1", "Alice", 50, False)
        self.highscore.add_game_result("player1", "Alice", 75, True)
        self.highscore.add_game_result("player1", "Alice", 60, False)

        stats = self.highscore.get_player_stats("player1")
        assert stats["best_score"] == 75

    def test_get_player_stats_nonexistent(self):
        """Test getting stats for nonexistent player."""
        stats = self.highscore.get_player_stats("nonexistent")
        assert stats == {}

    def test_get_top_players_empty(self):
        """Test getting top players when none exist."""
        top = self.highscore.get_top_players()
        assert top == []

    def test_get_top_players_single(self):
        """Test getting top players with single player."""
        self.highscore.add_game_result("player1", "Alice", 100, True)

        top = self.highscore.get_top_players()
        assert len(top) == 1
        assert top[0]["name"] == "Alice"
        assert top[0]["player_id"] == "player1"

    def test_get_top_players_multiple(self):
        """Test getting top players with multiple players."""
        self.highscore.add_game_result("player1", "Alice", 100, True)
        self.highscore.add_game_result("player2", "Bob", 80, False)
        self.highscore.add_game_result("player1", "Alice", 90, True)

        top = self.highscore.get_top_players()
        assert len(top) == 2
        # Alice should be first (2 wins vs 0)
        assert top[0]["name"] == "Alice"
        assert top[0]["games_won"] == 2

    def test_get_top_players_limit(self):
        """Test getting top players with limit."""
        for i in range(5):
            self.highscore.add_game_result(f"player{i}", f"Player{i}", 100, True)

        top = self.highscore.get_top_players(3)
        assert len(top) == 3

    def test_file_persistence(self):
        """Test that data persists to file."""
        self.highscore.add_game_result("player1", "Alice", 100, True)

        # Create new HighScore instance with same file
        new_highscore = HighScore(self.filename)
        stats = new_highscore.get_player_stats("player1")
        assert stats["name"] == "Alice"
        assert stats["games_won"] == 1

    def test_clear_all_scores(self):
        """Test clearing all scores."""
        self.highscore.add_game_result("player1", "Alice", 100, True)
        self.highscore.add_game_result("player2", "Bob", 80, False)

        self.highscore.clear_all_scores()
        assert len(self.highscore.get_all_scores()) == 0
        assert self.highscore.get_top_players() == []

    def test_get_all_scores(self):
        """Test getting all scores."""
        self.highscore.add_game_result("player1", "Alice", 100, True)
        self.highscore.add_game_result("player2", "Bob", 80, False)

        all_scores = self.highscore.get_all_scores()
        assert len(all_scores) == 2
        assert "player1" in all_scores
        assert "player2" in all_scores

    def test_corrupted_file_handling(self):
        """Test handling of corrupted score file."""
        # Write invalid JSON
        with open(self.filename, "w") as f:
            f.write("invalid json content")

        # Should handle gracefully
        highscore = HighScore(self.filename)
        assert len(highscore.get_all_scores()) == 0

    def test_win_percentage_sorting(self):
        """Test that players are sorted by wins then win percentage."""
        # Player 1: 2 wins out of 2 games (100%)
        self.highscore.add_game_result("player1", "Alice", 100, True)
        self.highscore.add_game_result("player1", "Alice", 100, True)

        # Player 2: 2 wins out of 3 games (66.7%)
        self.highscore.add_game_result("player2", "Bob", 100, True)
        self.highscore.add_game_result("player2", "Bob", 100, True)
        self.highscore.add_game_result("player2", "Bob", 50, False)

        top = self.highscore.get_top_players()
        # Both have 2 wins, but Alice has better percentage
        assert top[0]["name"] == "Alice"
        assert top[1]["name"] == "Bob"

    def test_last_played_timestamp(self):
        """Test that last played timestamp is recorded."""
        self.highscore.add_game_result("player1", "Alice", 100, True)

        stats = self.highscore.get_player_stats("player1")
        assert stats["last_played"] is not None
        assert isinstance(stats["last_played"], str)

    def test_multiple_games_statistics(self):
        """Test comprehensive statistics over multiple games."""
        # Simulate a series of games
        games = [(100, True), (75, False), (110, True), (65, False), (90, True)]

        for score, won in games:
            self.highscore.add_game_result("player1", "TestPlayer", score, won)

        stats = self.highscore.get_player_stats("player1")
        assert stats["games_played"] == 5
        assert stats["games_won"] == 3
        assert stats["total_points"] == 440
        assert stats["best_score"] == 110
