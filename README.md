# Pig Dice Game 

A Python implementation of the classic Pig dice game with AI opponents, persistent high scores, and comprehensive test coverage.

## About the Game

Pig is a simple dice game where players take turns rolling a die and accumulating points. The first player to reach 100 points wins!

### Rules
- Players take turns rolling a single die
- Each roll adds to the turn total
- Rolling a **1** ends your turn and you lose all points for that turn
- Choose to **hold** to bank your turn total and add it to your overall score
- First player to **100 points** wins!

### AI Intelligence Implementation

The game features three AI difficulty levels:

- **Easy (Timid)**: Conservative strategy, holds at 15+ points per turn
- **Medium (Balanced)**: Risk-based strategy, holds at 20-25 points depending on game state
- **Hard (Aggressive)**: Adaptive strategy that:
  - Considers score difference with opponent
  - Calculates risk vs reward
  - Becomes more aggressive when behind
  - Plays conservatively when ahead

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd pig-dice-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# OR
make install
```

## Running the Game

Execute the game using:
```bash
python main.py
```

Or use the Makefile:
```bash
make run
```

## Development

### Project Structure
```
pig-dice-game/
├── game/              # Game source code
│   ├── dice.py        # Dice class
│   ├── dice_hand.py   # DiceHand class
│   ├── player.py      # Player class
│   ├── intelligence.py # AI strategy
│   ├── highscore.py   # Persistent storage
│   ├── histogram.py   # Statistics visualization
│   ├── game.py        # Game logic
│   └── shell.py       # CLI interface
├── test/              # Unit tests
├── doc/               # Generated documentation
│   ├── api/          # API documentation
│   └── uml/          # UML diagrams
├── main.py           # Entry point
├── Makefile          # Build automation
└── requirements.txt  # Dependencies
```

### Running Tests

Run the complete test suite:
```bash
pytest
# OR
make test
```

Generate coverage report:
```bash
pytest --cov=game --cov-report=html --cov-report=term
# OR
make coverage
```

Coverage reports are generated in `htmlcov/index.html`.

### Code Style & Linting

Check code style:
```bash
make lint
```

This runs:
- **black** (code formatting check)
- **pylint** (code quality)
- **flake8** (style guide enforcement)

Format code:
```bash
black game/ test/
```

### Generating Documentation

#### API Documentation

Generate HTML documentation from docstrings:
```bash
make doc
```

Documentation is generated in `doc/api/index.html` using pdoc.

#### UML Diagrams

Generate UML class and package diagrams:
```bash
make uml
```

UML diagrams are created in `doc/uml/` directory using pyreverse (pylint).

View diagrams:
- `doc/uml/classes.png` - Class diagram
- `doc/uml/packages.png` - Package diagram

## Game Commands

Once the game starts, you can use these commands:

- `start` - Start a new game
- `roll` - Roll the dice
- `hold` - Hold and bank your points
- `scores` - View high scores
- `rules` - Display game rules
- `histogram` - Show dice roll statistics
- `name <new_name>` - Change your name
- `difficulty <easy|medium|hard>` - Set AI difficulty
- `cheat` - Activate cheat mode (adds 50 points)
- `quit` - Exit the game

## Features

 Single-player vs AI and two-player modes  
 Multiple AI difficulty levels  
 Persistent high score system  
 Player name management  
 Dice roll histogram/statistics  
 Clean text-based UI with UTF-8 characters  
 Input validation and error handling  
 Cheat mode for testing  

## Testing Statistics

- **Code Coverage**: >90%
- **Test Cases**: 10+ per class
- **Assertions**: 20+ per class
- **Testing Framework**: pytest

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## Authors

- suhasubasi - OMAR ALHAEK 

## Acknowledgments

- Game rules based on [Pig (dice game) - Wikipedia](https://en.wikipedia.org/wiki/Pig_(dice_game))