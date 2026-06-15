# Makefile для проекта A1_Maze_Py
# Стандартные GNU-цели: all, install, uninstall, clean, dvi, dist, tests

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest
INSTALL_DIR ?= $(HOME)/Maze_app
DIST_NAME := A1_Maze_Py

.PHONY: all install uninstall clean dvi dist tests run lint

# По умолчанию: создать окружение и поставить зависимости
all: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

# Запуск программы
run: all
	$(PY) -m src.main

# Установка: копируем код в $(INSTALL_DIR)
install: all
	mkdir -p $(INSTALL_DIR)
	cp -r src $(INSTALL_DIR)/
	cp -r examples $(INSTALL_DIR)/
	cp Makefile requirements.txt README.md $(INSTALL_DIR)/
	@echo "Установлено в $(INSTALL_DIR)"

# Удаление установленной версии
uninstall:
	rm -rf $(INSTALL_DIR)
	@echo "Удалено из $(INSTALL_DIR)"

# Чистка временных файлов
clean:
	rm -rf $(VENV)
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f $(DIST_NAME).tar.gz

# Документация (минимальная — копия README в текстовом виде)
dvi:
	@mkdir -p docs
	@cp README.md docs/documentation.md
	@echo "Документация в docs/documentation.md"

# Сборка дистрибутива (архива)
dist: clean
	tar --exclude='$(VENV)' --exclude='__pycache__' --exclude='.git' \
	    -czf $(DIST_NAME).tar.gz src tests examples Makefile requirements.txt README.md
	@echo "Архив: $(DIST_NAME).tar.gz"

# Запуск модульных тестов
tests: all
	$(PIP) install pytest pytest-cov
	$(PYTEST) tests/ -v --cov=src --cov-report=term-missing

# Линтер (проверка стиля Google по pylint)
lint: all
	$(PIP) install pylint
	$(VENV)/bin/pylint src/ --rcfile=.pylintrc || true
