#!/usr/bin/env python3
"""Main entry point for the Pig Dice Game application."""

from game.shell import GameShell


def main():
    """Start the Pig Dice Game application."""
    print("Welcome to Pig Dice Game!")
    print("Type 'help' for available commands")
    print("-" * 40)

    shell = GameShell()
    shell.cmdloop()


if __name__ == "__main__":
    main()
