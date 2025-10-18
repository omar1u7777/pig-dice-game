"""Command-line interface for the Pig dice game - COMPLETE VERSION."""

import cmd
from typing import Optional
from .game import Game
from .player import Player
from .intelligence import DifficultyLevel
from .highscore import HighScore
from .histogram import Histogram


class GameShell(cmd.Cmd):
    """Complete command-line interface for Pig dice game."""

    intro = """
🎲 Welcome to Pig Dice Game! 🎲
================================
Type 'help' to see all commands
Type 'rules' to learn how to play
Type 'start' to begin a new game
================================
"""
    prompt = "pig> "

    def __init__(self):
        """Initialize the game shell."""
        super().__init__()
        self.game: Optional[Game] = None
        self.highscore = HighScore()
        self.histogram = Histogram()
        self.cheat_mode = False

    # =================== GAME COMMANDS ===================

    def do_start(self, arg):
        """Start a new game.

        Usage: start [player_name]
        """
        player_name = arg.strip() if arg.strip() else "Player"

        print("\n🎮 Choose game mode:")
        print("1. Single player (vs Computer)")
        print("2. Two players")

        try:
            choice = input("Enter choice (1 or 2): ").strip()

            if choice == "1":
                # Single player vs AI
                human_player = Player(player_name, is_human=True)
                ai_player = Player("Computer", is_human=False)
                self.game = Game(human_player, ai_player)
                print(f"🎮 Started: {player_name} vs Computer")
            elif choice == "2":
                # Two human players
                player2_name = input("Enter Player 2 name: ").strip() or "Player 2"
                player1 = Player(player_name, is_human=True)
                player2 = Player(player2_name, is_human=True)
                self.game = Game(player1, player2)
                print(f"🎮 Started: {player_name} vs {player2_name}")
            else:
                print("❌ Invalid choice. Try again.")
                return

            self.game.start_game()
            self._show_game_status()

        except (KeyboardInterrupt, EOFError):
            print("\n❌ Game start cancelled.")

    def do_roll(self, arg):
        """Roll the dice."""
        if not self._check_game_active():
            return

        assert self.game is not None  # Ensure game is active for type checker

        current_player = self.game.get_current_player()
        if not current_player.is_human():
            print("❌ It's the computer's turn! Wait for AI to play.")
            return

        try:
            result = self.game.roll_dice()
            self.histogram.add_roll(result)

            if result == 1:
                print("💥 OH NO! Rolled a 1! Turn lost.")
            else:
                print(f"🎲 Rolled: {result}")

            self._show_game_status()
            self._check_for_winner()
            self._handle_ai_turn()

        except Exception as e:
            print(f"❌ Error: {e}")

    def do_hold(self, arg):
        """Hold and bank your points."""
        if not self._check_game_active():
            return

        assert self.game is not None  # Ensure game is active for type checker

        current_player = self.game.get_current_player()
        if not current_player.is_human():
            print("❌ It's the computer's turn!")
            return

        if current_player.get_turn_score() == 0:
            print("❌ No points to hold! Roll first.")
            return

        try:
            banked = self.game.hold_turn()
            print(f"💰 Banked {banked} points!")
            self._show_game_status()
            self._check_for_winner()
            self._handle_ai_turn()

        except Exception as e:
            print(f"❌ Error: {e}")

    def do_status(self, arg):
        """Show current game status."""
        if not self.game:
            print("❌ No game in progress. Use 'start' to begin.")
            return
        self._show_game_status()

    # =================== SETTINGS COMMANDS ===================

    def do_name(self, arg):
        """Change current player's name.

        Usage: name <new_name>
        """
        if not arg.strip():
            print("❌ Please provide a name. Usage: name <new_name>")
            return

        if not self.game:
            print("❌ No game in progress.")
            return

        try:
            current_player = self.game.get_current_player()
            if not current_player.is_human():
                print("❌ Cannot change computer player name.")
                return

            old_name = current_player.get_name()
            current_player.set_name(arg.strip())
            print(f"✅ Name changed from '{old_name}' to '{current_player.get_name()}'")
        except Exception as e:
            print(f"❌ Error: {e}")

    def do_difficulty(self, arg):
        """Set AI difficulty level.

        Usage: difficulty <easy|medium|hard>
        """
        if not arg.strip():
            print("❌ Usage: difficulty <easy|medium|hard>")
            return

        level = arg.strip().lower()
        if level not in ["easy", "medium", "hard"]:
            print("❌ Invalid difficulty. Use: easy, medium, or hard")
            return

        if self.game:
            difficulty_map = {
                "easy": DifficultyLevel.EASY,
                "medium": DifficultyLevel.MEDIUM,
                "hard": DifficultyLevel.HARD,
            }
            self.game.set_ai_difficulty(difficulty_map[level])

        print(f"🤖 AI difficulty set to: {level}")

    # =================== INFO COMMANDS ===================

    def do_rules(self, arg):
        """Show game rules."""
        print(
            """
🎲 PIG DICE GAME RULES
=======================

🎯 OBJECTIVE: 
   First player to reach 100 points wins!

🎮 HOW TO PLAY:
   1. Players take turns rolling a single die
   2. Each roll adds to your turn total
   3. Choose to 'roll' again or 'hold' to bank points

⚠️  THE RISK:
   Rolling a 1 loses ALL points for that turn!

💡 STRATEGY:
   Balance risk vs reward:
   - Keep rolling for more points (but risk losing all)
   - Hold early to secure points (but gain fewer)

🤖 AI DIFFICULTIES:
   - easy: Very conservative (holds at 15+ points)
   - medium: Balanced strategy (holds at ~20 points)
   - hard: Adaptive and aggressive strategy

📝 AVAILABLE COMMANDS:
   Game: start, roll, hold, status, quit
   Info: rules, scores, histogram, help
   Settings: name <name>, difficulty <level>
   Fun: cheat (adds 50 points for testing)

🏆 WINNING:
   First to 100 points wins!
   Your stats are saved automatically.
        """
        )

    def do_scores(self, arg):
        """Show high scores and statistics."""
        top_players = self.highscore.get_top_players(10)

        if not top_players:
            print("📊 No scores recorded yet. Play some games!")
            return

        print("\n🏆 HIGH SCORES & STATISTICS")
        print("=" * 50)
        print(
            f"{'Rank':<4} {'Name':<15} {'Wins':<5} {'Played':<7} {'Win%':<6} {'Best':<5}"
        )
        print("-" * 50)

        for i, stats in enumerate(top_players, 1):
            name = stats.get("name", "Unknown")[:14]
            wins = stats.get("games_won", 0)
            played = stats.get("games_played", 0)
            win_pct = (wins / played * 100) if played > 0 else 0
            best = stats.get("best_score", 0)

            print(f"{i:<4} {name:<15} {wins:<5} {played:<7} {win_pct:5.1f}% {best:<5}")

        print("=" * 50)

    def do_histogram(self, arg):
        """Show dice roll statistics."""
        print("\n" + self.histogram.display())
        print()

    # =================== FUN COMMANDS ===================

    def do_cheat(self, arg):
        """Activate cheat mode - adds 50 points for testing.

        Usage: cheat
        """
        if not self._check_game_active():
            return

        assert self.game is not None  # Ensure game is active for type checker

        current_player = self.game.get_current_player()
        if not current_player.is_human():
            print("❌ Cannot cheat for computer player!")
            return

        current_player.add_to_turn(50)
        self.cheat_mode = True
        print("🎭 CHEAT ACTIVATED! Added 50 points to current turn!")
        print("   (This is for testing purposes only)")
        self._show_game_status()

    # =================== SYSTEM COMMANDS ===================

    def do_quit(self, arg):
        """Quit the game."""
        print("\n👋 Thanks for playing Pig Dice Game!")
        print("🎲 Your scores have been saved.")
        return True

    def do_exit(self, arg):
        """Exit the game."""
        return self.do_quit(arg)

    def do_help(self, arg):
        """Show help for commands."""
        if arg:
            super().do_help(arg)
        else:
            print(
                """
🎲 PIG DICE GAME - AVAILABLE COMMANDS
======================================

🎮 GAME COMMANDS:
   start [name]     - Start new game
   roll             - Roll the dice
   hold             - Bank your turn points
   status           - Show current game status

📊 INFORMATION:
   rules            - Show game rules
   scores           - Show high scores
   histogram        - Show dice statistics
   help [command]   - Show help

⚙️  SETTINGS:
   name <new_name>  - Change your name
   difficulty <lvl> - Set AI difficulty (easy/medium/hard)

🎭 FUN:
   cheat            - Add 50 points (testing only)

🚪 EXIT:
   quit / exit      - Leave the game

Type 'help <command>' for specific command help.
            """
            )

    # =================== HELPER METHODS ===================

    def _check_game_active(self) -> bool:
        """Check if game is active."""
        if not self.game:
            print("❌ No game in progress. Use 'start' to begin.")
            return False
        if self.game.is_game_over():
            print("🏆 Game is over! Use 'start' for a new game.")
            return False
        return True

    def _show_game_status(self):
        """Display current game status with nice formatting."""
        if not self.game:
            return

        print("\n" + "=" * 60)
        print("🎯 GAME STATUS")
        print("=" * 60)

        player1, player2 = self.game.get_players()
        current = self.game.get_current_player()

        # Show both players
        for player in [player1, player2]:
            symbol = "👤" if player.is_human() else "🤖"
            status = " 👈 CURRENT TURN" if player == current else ""
            total = player.get_total_score()
            turn = player.get_turn_score()

            print(f"{symbol} {player.get_name()}: {total} points", end="")
            if turn > 0:
                print(f" + {turn} turn points", end="")
            print(status)

        print(f"\n🎯 Target: {self.game.get_winning_score()} points")

        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner is not None:
                print(f"🏆 WINNER: {winner.get_name()}! 🎉")
            if self.cheat_mode:
                print("🎭 (Cheat mode was used this game)")
        else:
            print(f"\n🎲 {current.get_name()}'s turn")
            if current.get_turn_score() > 0:
                print(f"💰 Current turn: {current.get_turn_score()} points")

            if not current.is_human():
                print("🤖 Computer is thinking...")

        print("=" * 60)

    def _handle_ai_turn(self):
        """Handle AI player's automatic turn."""
        if not self.game or self.game.is_game_over():
            return

        current_player = self.game.get_current_player()
        if current_player.is_human():
            return

        import time

        print("\n🤖 Computer is playing...")
        time.sleep(1)  # Dramatic pause

        # AI plays automatically
        while (
            not self.game.is_game_over()
            and not self.game.get_current_player().is_human()
        ):

            # AI decides
            should_roll = self.game.ai_should_roll()

            if should_roll:
                result = self.game.roll_dice()
                self.histogram.add_roll(result)

                if result == 1:
                    print("🤖💥 Computer rolled a 1! Turn lost.")
                    break
                else:
                    print(f"🤖🎲 Computer rolled: {result}")
                    time.sleep(0.8)
            else:
                banked = self.game.hold_turn()
                print(f"🤖💰 Computer holds and banks {banked} points!")
                break

        self._show_game_status()
        self._check_for_winner()

    def _check_for_winner(self):
        """Check for winner and save scores."""
        if not self.game or not self.game.is_game_over():
            return

        winner = self.game.get_winner()
        player1, player2 = self.game.get_players()

        # Save both players' results
        for player in [player1, player2]:
            if hasattr(player, "_player_id"):  # Has ID for persistence
                won = player == winner
                self.highscore.add_game_result(
                    player._player_id, player.get_name(), player.get_total_score(), won
                )

        # Reset cheat mode
        self.cheat_mode = False
