"""HighScore module for persistent storage of player statistics.

This module manages the high score system with persistent JSON storage,
allowing player statistics to survive across game sessions and name changes.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class HighScore:
    """Manages persistent high scores and player statistics.

    This class handles saving and loading player statistics to/from a JSON file.
    Statistics are tied to unique player IDs, allowing names to change while
    preserving the statistical history.

    Attributes:
        _filename (str): Path to the JSON file for storage
        _scores (Dict[str, Dict[str, Any]]): In-memory scores dictionary
    """

    def __init__(self, filename: str = "highscores.json") -> None:
        """Initialize high score manager.

        Args:
            filename (str): JSON file to store scores. Defaults to "highscores.json".
        """
        self._filename = filename
        self._scores: Dict[str, Dict[str, Any]] = {}
        self._load_scores()

    def _load_scores(self) -> None:
        """Load scores from file.

        If the file doesn't exist or contains invalid JSON,
        an empty scores dictionary is initialized.
        """
        if os.path.exists(self._filename):
            try:
                with open(self._filename, "r", encoding="utf-8") as f:
                    self._scores = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._scores = {}
        else:
            self._scores = {}

    def _save_scores(self) -> None:
        """Save scores to file.

        Writes the current scores dictionary to the JSON file.
        Fails silently if there are file permission issues.
        """
        try:
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(self._scores, f, indent=2)
        except IOError:
            pass  # Fail silently if can't save

    def add_game_result(
        self, player_id: str, player_name: str, final_score: int, won: bool
    ) -> None:
        """Add a game result for a player.

        Args:
            player_id (str): Unique player ID
            player_name (str): Player's current name
            final_score (int): Final score achieved in the game
            won (bool): Whether the player won the game
        """
        if player_id not in self._scores:
            self._scores[player_id] = {
                "name": player_name,
                "games_played": 0,
                "games_won": 0,
                "total_points": 0,
                "best_score": 0,
                "last_played": None,
            }

        stats = self._scores[player_id]
        stats["name"] = player_name  # Update name (allows name changes)
        stats["games_played"] += 1
        stats["total_points"] += final_score
        stats["last_played"] = datetime.now().isoformat()

        if won:
            stats["games_won"] += 1

        if final_score > stats["best_score"]:
            stats["best_score"] = final_score

        self._save_scores()

    def get_player_stats(self, player_id: str) -> Dict[str, Any]:
        """Get statistics for a specific player.

        Args:
            player_id (str): Unique player ID

        Returns:
            Dict[str, Any]: Dictionary with player statistics, or empty dict if not found
        """
        return self._scores.get(player_id, {})

    def get_top_players(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top players sorted by games won and win percentage.

        Args:
            limit (int): Maximum number of players to return. Defaults to 10.

        Returns:
            List[Dict[str, Any]]: List of player statistics sorted by performance
        """
        all_stats = []
        for player_id, stats in self._scores.items():
            stats_copy = stats.copy()
            stats_copy["player_id"] = player_id
            all_stats.append(stats_copy)

        # Sort by games won (primary), then by win percentage (secondary)
        def sort_key(stats):
            wins = stats.get("games_won", 0)
            played = stats.get("games_played", 1)
            win_pct = wins / played if played > 0 else 0
            return (wins, win_pct)

        return sorted(all_stats, key=sort_key, reverse=True)[:limit]

    def clear_all_scores(self) -> None:
        """Clear all saved scores and save empty state to file."""
        self._scores = {}
        self._save_scores()

    def get_all_scores(self) -> Dict[str, Dict[str, Any]]:
        """Get all scores.

        Returns:
            Dict[str, Dict[str, Any]]: Copy of all scores dictionary
        """
        return self._scores.copy()

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: Description of high score manager
        """
        return f"HighScore({len(self._scores)} players)"
