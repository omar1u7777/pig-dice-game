.PHONY: install test coverage lint doc uml clean run format help

help:
	@echo "🎲 Pig Dice Game - Available Commands:"
	@echo "  install   - Install dependencies"
	@echo "  run       - Run the game"
	@echo "  test      - Run test suite"
	@echo "  coverage  - Generate coverage report"
	@echo "  lint      - Run linters"
	@echo "  format    - Format code with black"
	@echo "  doc       - Generate API documentation"
	@echo "  uml       - Generate UML diagrams"
	@echo "  clean     - Remove generated files"

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest -v

coverage:
	pytest --cov=game --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report: htmlcov/index.html"

lint:
	@echo "🔍 Running code quality checks..."
	black --check game/ test/ main.py || exit /b 0
	pylint game/ test/ main.py || exit /b 0
	flake8 game/ test/ main.py || exit /b 0

format:
	black game/ test/ main.py

doc:
	@echo "📚 Generating API documentation..."
	powershell -Command "New-Item -Path doc/api -ItemType Directory -Force"
	pdoc --out doc/api game
	@echo "✅ Documentation: doc/api/game/index.html"

uml:
	@echo "📐 Generating UML diagrams..."
	powershell -Command "New-Item -Path doc/uml -ItemType Directory -Force"
	pyreverse -o png -p pig-game game/ -d doc/uml --show-ancestors 3 --show-associated 3
	@echo "✅ UML diagrams: doc/uml/"

clean:
	@echo "🧹 Cleaning up generated files..."
	-powershell -Command "Get-ChildItem -Path . -Include '__pycache__' -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
	-powershell -Command "Remove-Item -Path '.pytest_cache','htmlcov','.coverage' -Recurse -Force -ErrorAction SilentlyContinue"
	-powershell -Command "Remove-Item -Path 'doc/api/*','doc/uml/*' -Recurse -Force -ErrorAction SilentlyContinue"
	-powershell -Command "Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue"
	-powershell -Command "Get-ChildItem -Path . -Filter *.pyo -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue"