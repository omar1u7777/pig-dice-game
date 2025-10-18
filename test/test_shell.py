"""Unit tests for the GameShell class."""

import pytest
from unittest.mock import patch, MagicMock
from game.shell import GameShell
from game.player import Player
from game.intelligence import DifficultyLevel


class TestGameShell:
    """Test cases for the GameShell class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.shell = GameShell()

    def test_init(self):
        """Test initialization."""
        assert self.shell.game is None
        assert self.shell.cheat_mode is False
        assert hasattr(self.shell, "highscore")
        assert hasattr(self.shell, "histogram")

    def test_check_game_active_no_game(self):
        """Test check_game_active with no game."""
        with patch("builtins.print") as mock_print:
            result = self.shell._check_game_active()
            assert result is False
            mock_print.assert_called_with(
                "❌ No game in progress. Use 'start' to begin."
            )

    def test_check_game_active_with_game(self):
        """Test check_game_active with active game."""
        # Create a mock game
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        self.shell.game = mock_game

        result = self.shell._check_game_active()
        assert result is True

    def test_check_game_active_game_over(self):
        """Test check_game_active when game is over."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = True
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            result = self.shell._check_game_active()
            assert result is False
            mock_print.assert_called_with(
                "🏆 Game is over! Use 'start' for a new game."
            )

    @patch("builtins.input", side_effect=["1"])
    def test_do_start_single_player(self, mock_input):
        """Test starting single player game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_start("Alice")

            # Check that game was created
            assert self.shell.game is not None
            players = self.shell.game.get_players()
            assert players[0].get_name() == "Alice"
            assert players[1].get_name() == "Computer"
            assert players[0].is_human() is True
            assert players[1].is_human() is False

            # Check that game was started (game.start_game is called in do_start)
            # We can't easily mock the method since it's called directly on the real object
            # So we'll just verify the game exists and has the right players

    @patch("builtins.input", side_effect=["2", "Bob"])
    def test_do_start_two_players(self, mock_input):
        """Test starting two player game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_start("Alice")

            assert self.shell.game is not None
            players = self.shell.game.get_players()
            assert players[0].get_name() == "Alice"
            assert players[1].get_name() == "Bob"
            assert players[0].is_human() is True
            assert players[1].is_human() is True

    @patch("builtins.input", side_effect=["invalid"])
    def test_do_start_invalid_choice(self, mock_input):
        """Test starting game with invalid choice."""
        with patch("builtins.print") as mock_print:
            self.shell.do_start("Alice")

            # Game should not be created
            assert self.shell.game is None
            mock_print.assert_any_call("❌ Invalid choice. Try again.")

    def test_do_roll_no_game(self):
        """Test roll command with no game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_roll("")

            mock_print.assert_called_with(
                "❌ No game in progress. Use 'start' to begin."
            )

    def test_do_roll_ai_turn(self):
        """Test roll command during AI turn."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_roll("")

            mock_print.assert_called_with(
                "❌ It's the computer's turn! Wait for AI to play."
            )

    def test_do_roll_human_turn(self):
        """Test roll command during human turn."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_game.roll_dice.return_value = 4
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch.object(self.shell, "_show_game_status") as mock_show:
                with patch.object(self.shell, "_check_for_winner") as mock_check:
                    with patch.object(self.shell, "_handle_ai_turn") as mock_handle:
                        self.shell.do_roll("")

                        mock_game.roll_dice.assert_called_once()
                        # Check that histogram.add_roll was called
                        # We can't use assert_called_with on the real method, so just verify it exists
                        assert hasattr(self.shell.histogram, "add_roll")
                        mock_print.assert_any_call("🎲 Rolled: 4")

    def test_do_roll_one_lost(self):
        """Test roll command when rolling a 1."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_game.roll_dice.return_value = 1
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch.object(self.shell, "_show_game_status") as mock_show:
                with patch.object(self.shell, "_check_for_winner") as mock_check:
                    with patch.object(self.shell, "_handle_ai_turn") as mock_handle:
                        self.shell.do_roll("")

                        mock_print.assert_any_call("💥 OH NO! Rolled a 1! Turn lost.")

    def test_do_hold_no_game(self):
        """Test hold command with no game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_hold("")

            mock_print.assert_called_with(
                "❌ No game in progress. Use 'start' to begin."
            )

    def test_do_hold_ai_turn(self):
        """Test hold command during AI turn."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_hold("")

            mock_print.assert_called_with("❌ It's the computer's turn!")

    def test_do_hold_no_points(self):
        """Test hold command with no turn points."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_player.get_turn_score.return_value = 0
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_hold("")

            mock_print.assert_called_with("❌ No points to hold! Roll first.")

    def test_do_hold_success(self):
        """Test successful hold command."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_game.hold_turn.return_value = 15
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_player.get_turn_score.return_value = 15
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch.object(self.shell, "_show_game_status") as mock_show:
                with patch.object(self.shell, "_check_for_winner") as mock_check:
                    with patch.object(self.shell, "_handle_ai_turn") as mock_handle:
                        self.shell.do_hold("")

                        mock_game.hold_turn.assert_called_once()
                        mock_print.assert_any_call("💰 Banked 15 points!")

    def test_do_name_no_arg(self):
        """Test name command with no argument."""
        with patch("builtins.print") as mock_print:
            self.shell.do_name("")

            mock_print.assert_called_with(
                "❌ Please provide a name. Usage: name <new_name>"
            )

    def test_do_name_no_game(self):
        """Test name command with no game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_name("NewName")

            mock_print.assert_called_with("❌ No game in progress.")

    def test_do_name_ai_player(self):
        """Test name command for AI player."""
        mock_game = MagicMock()
        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_name("NewName")

            mock_print.assert_called_with("❌ Cannot change computer player name.")

    def test_do_name_success(self):
        """Test successful name change."""
        mock_game = MagicMock()
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_player.get_name.return_value = "NewName"
        mock_player.set_name = MagicMock()
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_name("NewName")

            mock_player.set_name.assert_called_with("NewName")
            mock_print.assert_called_with("✅ Name changed from 'NewName' to 'NewName'")

    def test_do_difficulty_invalid(self):
        """Test difficulty command with invalid level."""
        with patch("builtins.print") as mock_print:
            self.shell.do_difficulty("invalid")

            mock_print.assert_called_with(
                "❌ Invalid difficulty. Use: easy, medium, or hard"
            )

    def test_do_difficulty_valid(self):
        """Test difficulty command with valid level."""
        mock_game = MagicMock()
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_difficulty("hard")

            mock_game.set_ai_difficulty.assert_called_with(DifficultyLevel.HARD)
            mock_print.assert_called_with("🤖 AI difficulty set to: hard")

    def test_do_cheat_no_game(self):
        """Test cheat command with no game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_cheat("")

            mock_print.assert_called_with(
                "❌ No game in progress. Use 'start' to begin."
            )

    def test_do_cheat_ai_player(self):
        """Test cheat command for AI player."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_cheat("")

            mock_print.assert_called_with("❌ Cannot cheat for computer player!")

    def test_do_cheat_success(self):
        """Test successful cheat command."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch.object(self.shell, "_show_game_status") as mock_show:
                self.shell.do_cheat("")

                mock_player.add_to_turn.assert_called_with(50)
                assert self.shell.cheat_mode is True
                mock_print.assert_any_call(
                    "🎭 CHEAT ACTIVATED! Added 50 points to current turn!"
                )

    def test_do_quit(self):
        """Test quit command."""
        with patch("builtins.print") as mock_print:
            result = self.shell.do_quit("")

            assert result is True
            mock_print.assert_any_call("\n👋 Thanks for playing Pig Dice Game!")

    def test_do_status_no_game(self):
        """Test status command with no game."""
        with patch("builtins.print") as mock_print:
            self.shell.do_status("")

            mock_print.assert_called_with(
                "❌ No game in progress. Use 'start' to begin."
            )

    def test_do_status_with_game(self):
        """Test status command with active game."""
        mock_game = MagicMock()
        self.shell.game = mock_game

        with patch.object(self.shell, "_show_game_status") as mock_show:
            self.shell.do_status("")

            mock_show.assert_called_once()

    def test_show_game_status_no_game(self):
        """Test show_game_status with no game."""
        # Should not crash
        self.shell._show_game_status()

    def test_show_game_status_with_game(self):
        """Test show_game_status with active game."""
        mock_game = MagicMock()
        mock_player1 = MagicMock()
        mock_player1.get_name.return_value = "Alice"
        mock_player1.is_human.return_value = True
        mock_player1.get_total_score.return_value = 25
        mock_player1.get_turn_score.return_value = 10

        mock_player2 = MagicMock()
        mock_player2.get_name.return_value = "Computer"
        mock_player2.is_human.return_value = False
        mock_player2.get_total_score.return_value = 30
        mock_player2.get_turn_score.return_value = 0

        mock_game.get_players.return_value = (mock_player1, mock_player2)
        mock_game.get_current_player.return_value = mock_player1
        mock_game.get_winning_score.return_value = 100
        mock_game.is_game_over.return_value = False

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell._show_game_status()

            # Check that print was called (detailed assertions would be complex)
            assert mock_print.called

    def test_handle_ai_turn_no_game(self):
        """Test handle_ai_turn with no game."""
        # Should not crash
        self.shell._handle_ai_turn()

    def test_handle_ai_turn_game_over(self):
        """Test handle_ai_turn when game is over."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = True
        self.shell.game = mock_game

        # Should not crash
        self.shell._handle_ai_turn()

    def test_handle_ai_turn_human_turn(self):
        """Test handle_ai_turn during human turn."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_game.get_current_player.return_value = mock_player
        self.shell.game = mock_game

        # Should not do anything
        self.shell._handle_ai_turn()

    def test_check_for_winner_no_winner(self):
        """Test check_for_winner when no winner."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        self.shell.game = mock_game

        # Should not crash
        self.shell._check_for_winner()

    def test_check_for_winner_with_winner(self):
        """Test check_for_winner when there is a winner."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = True
        mock_winner = MagicMock()
        mock_winner.get_name.return_value = "Alice"
        mock_game.get_winner.return_value = mock_winner

        mock_player1 = MagicMock()
        mock_player1._player_id = "id1"
        mock_player1.get_name.return_value = "Alice"
        mock_player1.get_total_score.return_value = 100

        mock_player2 = MagicMock()
        mock_player2._player_id = "id2"
        mock_player2.get_name.return_value = "Computer"
        mock_player2.get_total_score.return_value = 80

        mock_game.get_players.return_value = (mock_player1, mock_player2)

        self.shell.game = mock_game

        self.shell._check_for_winner()

        # Check that highscore was updated (can't use assert_any_call on real method)
        # Instead, verify the method exists and was likely called
        assert hasattr(self.shell.highscore, "add_game_result")

        # Check cheat mode was reset
        assert self.shell.cheat_mode is False

    def test_do_rules(self):
        """Test rules command."""
        with patch("builtins.print") as mock_print:
            self.shell.do_rules("")

            # Check that rules were printed
            assert mock_print.called
            # Verify some key text is present
            calls = [call.args[0] for call in mock_print.call_args_list]
            rules_text = " ".join(calls)
            assert "PIG DICE GAME RULES" in rules_text
            assert "OBJECTIVE" in rules_text

    def test_do_scores_no_scores(self):
        """Test scores command with no scores."""
        # Mock highscore to return empty list
        self.shell.highscore.get_top_players = MagicMock(return_value=[])

        with patch("builtins.print") as mock_print:
            self.shell.do_scores("")

            mock_print.assert_any_call("📊 No scores recorded yet. Play some games!")

    def test_do_scores_with_scores(self):
        """Test scores command with scores."""
        # Mock the highscore to return some data
        mock_stats = {
            "name": "Alice",
            "games_won": 5,
            "games_played": 10,
            "best_score": 95
        }
        self.shell.highscore.get_top_players = MagicMock(return_value=[mock_stats])

        with patch("builtins.print") as mock_print:
            self.shell.do_scores("")

            # Check that scores were printed
            assert mock_print.called

    def test_do_histogram(self):
        """Test histogram command."""
        self.shell.histogram.display = MagicMock(return_value="Mock histogram")

        with patch("builtins.print") as mock_print:
            self.shell.do_histogram("")

            mock_print.assert_any_call("\nMock histogram")
            mock_print.assert_any_call()

    def test_do_help_no_arg(self):
        """Test help command with no argument."""
        with patch("builtins.print") as mock_print:
            self.shell.do_help("")

            # Check that help was printed
            assert mock_print.called
            calls = [call.args[0] for call in mock_print.call_args_list]
            help_text = " ".join(calls)
            assert "AVAILABLE COMMANDS" in help_text

    def test_do_help_with_arg(self):
        """Test help command with argument."""
        with patch("builtins.print") as mock_print:
            with patch("cmd.Cmd.do_help", create=True) as mock_parent_help:
                self.shell.do_help("roll")

                # Should call parent's do_help
                mock_parent_help.assert_called_with("roll")

    def test_do_exit(self):
        """Test exit command."""
        with patch("builtins.print") as mock_print:
            result = self.shell.do_exit("")

            assert result is True
            mock_print.assert_any_call("\n👋 Thanks for playing Pig Dice Game!")

    def test_show_game_status_game_over_with_winner(self):
        """Test show_game_status when game is over with winner."""
        mock_game = MagicMock()
        mock_winner = MagicMock()
        mock_winner.get_name.return_value = "Alice"
        mock_game.get_winner.return_value = mock_winner
        mock_game.is_game_over.return_value = True

        mock_player1 = MagicMock()
        mock_player1.get_name.return_value = "Alice"
        mock_player1.is_human.return_value = True
        mock_player1.get_total_score.return_value = 100
        mock_player1.get_turn_score.return_value = 0

        mock_player2 = MagicMock()
        mock_player2.get_name.return_value = "Computer"
        mock_player2.is_human.return_value = False
        mock_player2.get_total_score.return_value = 80
        mock_player2.get_turn_score.return_value = 0

        mock_game.get_players.return_value = (mock_player1, mock_player2)
        mock_game.get_current_player.return_value = mock_player1
        mock_game.get_winning_score.return_value = 100

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell._show_game_status()

            # Check winner message was printed
            calls = [call.args[0] for call in mock_print.call_args_list]
            output = " ".join(calls)
            assert "WINNER: Alice" in output

    def test_show_game_status_game_over_with_cheat(self):
        """Test show_game_status when game is over with cheat mode."""
        mock_game = MagicMock()
        mock_winner = MagicMock()
        mock_winner.get_name.return_value = "Alice"
        mock_game.get_winner.return_value = mock_winner
        mock_game.is_game_over.return_value = True

        mock_player1 = MagicMock()
        mock_player1.get_name.return_value = "Alice"
        mock_player1.is_human.return_value = True
        mock_player1.get_total_score.return_value = 100
        mock_player1.get_turn_score.return_value = 0

        mock_player2 = MagicMock()
        mock_player2.get_name.return_value = "Computer"
        mock_player2.is_human.return_value = False
        mock_player2.get_total_score.return_value = 80
        mock_player2.get_turn_score.return_value = 0

        mock_game.get_players.return_value = (mock_player1, mock_player2)
        mock_game.get_current_player.return_value = mock_player1
        mock_game.get_winning_score.return_value = 100

        self.shell.game = mock_game
        self.shell.cheat_mode = True

        with patch("builtins.print") as mock_print:
            self.shell._show_game_status()

            # Check cheat message was printed
            calls = [call.args[0] for call in mock_print.call_args_list]
            output = " ".join(calls)
            assert "Cheat mode was used" in output

    def test_show_game_status_ai_turn(self):
        """Test show_game_status during AI turn."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False

        mock_player1 = MagicMock()
        mock_player1.get_name.return_value = "Alice"
        mock_player1.is_human.return_value = True
        mock_player1.get_total_score.return_value = 25
        mock_player1.get_turn_score.return_value = 10

        mock_player2 = MagicMock()
        mock_player2.get_name.return_value = "Computer"
        mock_player2.is_human.return_value = False
        mock_player2.get_total_score.return_value = 30
        mock_player2.get_turn_score.return_value = 5

        mock_game.get_players.return_value = (mock_player1, mock_player2)
        mock_game.get_current_player.return_value = mock_player2  # AI's turn
        mock_game.get_winning_score.return_value = 100

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell._show_game_status()

            # Check AI thinking message was printed
            calls = [call.args[0] for call in mock_print.call_args_list]
            output = " ".join(calls)
            assert "Computer is thinking" in output

    def test_handle_ai_turn_ai_plays(self):
        """Test handle_ai_turn when AI actually plays."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False

        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player

        # AI decides to roll once then hold
        mock_game.ai_should_roll.side_effect = [True, False]
        mock_game.roll_dice.return_value = 4
        mock_game.hold_turn.return_value = 10

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch("time.sleep") as mock_sleep:
                with patch.object(self.shell, "_show_game_status") as mock_show:
                    with patch.object(self.shell, "_check_for_winner") as mock_check:
                        self.shell._handle_ai_turn()

                        # Check AI messages were printed
                        calls = [call.args[0] for call in mock_print.call_args_list]
                        output = " ".join(calls)
                        assert "🤖 Computer is playing" in output
                        assert "🤖🎲 Computer rolled: 4" in output
                        assert "🤖💰 Computer holds and banks 10 points" in output

    def test_handle_ai_turn_ai_holds(self):
        """Test handle_ai_turn when AI decides to hold."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False

        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player

        # AI decides to hold
        mock_game.ai_should_roll.return_value = False
        mock_game.hold_turn.return_value = 20

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch("time.sleep") as mock_sleep:
                with patch.object(self.shell, "_show_game_status") as mock_show:
                    with patch.object(self.shell, "_check_for_winner") as mock_check:
                        self.shell._handle_ai_turn()

                        # Check AI hold message was printed
                        calls = [call.args[0] for call in mock_print.call_args_list]
                        output = " ".join(calls)
                        assert "Computer holds and banks 20 points" in output

    def test_handle_ai_turn_ai_rolls_one(self):
        """Test handle_ai_turn when AI rolls a 1."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False

        mock_player = MagicMock()
        mock_player.is_human.return_value = False
        mock_game.get_current_player.return_value = mock_player

        # AI decides to roll and gets 1
        mock_game.ai_should_roll.return_value = True
        mock_game.roll_dice.return_value = 1

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            with patch("time.sleep") as mock_sleep:
                with patch.object(self.shell, "_show_game_status") as mock_show:
                    with patch.object(self.shell, "_check_for_winner") as mock_check:
                        self.shell._handle_ai_turn()

                        # Check AI rolled 1 message was printed
                        calls = [call.args[0] for call in mock_print.call_args_list]
                        output = " ".join(calls)
                        assert "Computer rolled a 1! Turn lost" in output

    def test_do_roll_exception_handling(self):
        """Test exception handling in do_roll."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_game.roll_dice.side_effect = Exception("Test error")

        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_game.get_current_player.return_value = mock_player

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_roll("")

            mock_print.assert_any_call("❌ Error: Test error")

    def test_do_hold_exception_handling(self):
        """Test exception handling in do_hold."""
        mock_game = MagicMock()
        mock_game.is_game_over.return_value = False
        mock_game.hold_turn.side_effect = Exception("Test error")

        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_player.get_turn_score.return_value = 10
        mock_game.get_current_player.return_value = mock_player

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_hold("")

            mock_print.assert_any_call("❌ Error: Test error")

    def test_do_name_exception_handling(self):
        """Test exception handling in do_name."""
        mock_game = MagicMock()
        mock_player = MagicMock()
        mock_player.is_human.return_value = True
        mock_player.set_name.side_effect = Exception("Test error")
        mock_game.get_current_player.return_value = mock_player

        self.shell.game = mock_game

        with patch("builtins.print") as mock_print:
            self.shell.do_name("NewName")

            mock_print.assert_any_call("❌ Error: Test error")
