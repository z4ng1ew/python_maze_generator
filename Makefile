PYTHON = python3
INSTALL_DIR ?= $(HOME)/maze_app
PYTEST = pytest

.PHONY: all install uninstall clean dvi dist tests

all:
	@echo "Project is ready"
	python main.py

install:
	pip install -r requirements.txt
	mkdir -p $(INSTALL_DIR)
	cp -r generator $(INSTALL_DIR)/
	cp -r rendering $(INSTALL_DIR)/
	cp -r dataSorce $(INSTALL_DIR)/
	cp main.py maze.py $(INSTALL_DIR)/

uninstall:
	rm -rf $(INSTALL_DIR)
	@echo "Removed $(INSTALL_DIR)"

tests:
	pytest -v
	$(PYTEST) --cov=generator --cov-report=html

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

dvi:
	@echo "Maze project"
	@echo "Run: python3 main.py"

dist:
	mkdir -p dist
	tar -czf dist/maze_project.tar.gz \
		generator \
		dataSorce \
		rendering \
		tests \
		main.py \
		maze.py \
		Makefile \
		requirements.txt
	@echo "Archive created: dist/maze_project.tar.gz"

