"""Test to verify all assignment requirements are met."""

import pytest
import os
import importlib
from pathlib import Path


class TestRequirements:
    """Test that all assignment requirements are fulfilled."""

    def test_all_required_classes_exist(self):
        """Test that all required classes exist."""
        required_classes = [
            "game.dice.Dice",
            "game.dice_hand.DiceHand",
            "game.player.Player",
            "game.intelligence.Intelligence",
            "game.highscore.HighScore",
            "game.histogram.Histogram",
            "game.game.Game",
            "game.shell.GameShell",
        ]

        for class_path in required_classes:
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            assert hasattr(
                module, class_name
            ), f"Class {class_name} not found in {module_name}"

    def test_project_structure(self):
        """Test that project has correct structure."""
        required_files = [
            "main.py",
            "requirements.txt",
            "Makefile",
            "README.md",
            "LICENSE.md",
            ".pylintrc",
            ".flake8",
            ".gitignore",
            "game/__init__.py",
            "test/__init__.py",
        ]

        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} not found"

    def test_test_file_coverage(self):
        """Test that all classes have corresponding test files."""
        test_files = [
            "test/test_dice.py",
            "test/test_dice_hand.py",
            "test/test_player.py",
            "test/test_intelligence.py",
            "test/test_highscore.py",
            "test/test_histogram.py",
            "test/test_game.py",
        ]

        for test_file in test_files:
            assert os.path.exists(test_file), f"Test file {test_file} not found"

    def test_minimum_test_cases_per_class(self):
        """Test that each test class has at least 10 test methods."""
        test_classes = [
            "test.test_dice.TestDice",
            "test.test_dice_hand.TestDiceHand",
            "test.test_player.TestPlayer",
            "test.test_intelligence.TestIntelligence",
            "test.test_highscore.TestHighScore",
            "test.test_histogram.TestHistogram",
            "test.test_game.TestGame",
        ]

        for class_path in test_classes:
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            test_class = getattr(module, class_name)

            test_methods = [
                method for method in dir(test_class) if method.startswith("test_")
            ]

            assert (
                len(test_methods) >= 10
            ), f"{class_name} has only {len(test_methods)} test methods, need at least 10"

    def test_docstring_coverage(self):
        """Test that all classes and methods have docstrings."""
        import game.dice
        import game.player
        import game.game

        # Test a few key classes have docstrings
        assert game.dice.Dice.__doc__ is not None
        assert game.player.Player.__doc__ is not None
        assert game.game.Game.__doc__ is not None

        # Test key methods have docstrings
        assert game.dice.Dice.roll.__doc__ is not None
        assert game.player.Player.add_to_turn.__doc__ is not None
        assert game.game.Game.roll_dice.__doc__ is not None

    def test_cmd_interface_exists(self):
        """Test that cmd interface is implemented."""
        from game.shell import GameShell
        import cmd

        assert issubclass(GameShell, cmd.Cmd), "GameShell must inherit from cmd.Cmd"

        # Check for required command methods
        required_commands = ["do_start", "do_roll", "do_hold", "do_rules", "do_quit"]
        for command in required_commands:
            assert hasattr(GameShell, command), f"Missing command: {command}"

    def test_ai_difficulty_levels(self):
        """Test that AI has multiple difficulty levels."""
        from game.intelligence import Intelligence, DifficultyLevel

        # Test all difficulty levels exist
        assert hasattr(DifficultyLevel, "EASY")
        assert hasattr(DifficultyLevel, "MEDIUM")
        assert hasattr(DifficultyLevel, "HARD")

        # Test AI can be created with different difficulties
        easy_ai = Intelligence(DifficultyLevel.EASY)
        medium_ai = Intelligence(DifficultyLevel.MEDIUM)
        hard_ai = Intelligence(DifficultyLevel.HARD)

        assert easy_ai.get_difficulty() == DifficultyLevel.EASY
        assert medium_ai.get_difficulty() == DifficultyLevel.MEDIUM
        assert hard_ai.get_difficulty() == DifficultyLevel.HARD

    def test_persistent_storage(self):
        """Test that high score system uses persistent storage."""
        from game.highscore import HighScore
        import tempfile
        import os

        # Test with temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name

        try:
            hs = HighScore(tmp_name)
            hs.add_game_result("test_id", "TestPlayer", 100, True)

            # Create new instance - should load data
            hs2 = HighScore(tmp_name)
            stats = hs2.get_player_stats("test_id")
            assert stats["name"] == "TestPlayer"

        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def test_game_features_complete(self):
        """Test that all required game features are implemented."""
        from game.game import Game
        from game.player import Player
        from game.shell import GameShell

        # Test two-player support
        p1 = Player("Human", is_human=True)
        p2 = Player("AI", is_human=False)
        game = Game(p1, p2)

        # Test basic game operations
        game.start_game()
        assert not game.is_game_over()

        # Test shell has all required commands
        shell = GameShell()
        required_commands = [
            "start",
            "roll",
            "hold",
            "rules",
            "scores",
            "cheat",
            "quit",
        ]
        for cmd in required_commands:
            assert hasattr(shell, f"do_{cmd}"), f"Missing shell command: {cmd}"
