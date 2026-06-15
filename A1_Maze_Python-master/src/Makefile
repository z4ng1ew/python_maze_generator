.PHONY: all install uninstall clean fclean dvi dist tests format check cov venv
PYTHON=python3.11
VENV=.venv
PYEXEC=poetry run

all: install

install:
	$(PYEXEC) pyinstaller --onefile --windowed main.py
	./dist/main

uninstall:
	rm -r dist

clean:
	rm -rf build *cache* .*cache dist .coverage htmlcov

fclean: clean
	rm -rf $(VENV)

dvi:
	open README.md

dist: install
	tar -czf dist.tar.gz dist

format:
	$(PYEXEC) isort .
	$(PYEXEC) ruff format .

check:
	$(PYEXEC) ruff check

tests:
	$(PYEXEC) pytest #-W ignore::DeprecationWarning

cov:
	$(PYEXEC) pytest --cov --cov-report=html #-W ignore::DeprecationWarning
	open htmlcov/index.html

venv:
	poetry env use $(PYTHON)
	poetry install

run:
	$(PYEXEC) python main.py