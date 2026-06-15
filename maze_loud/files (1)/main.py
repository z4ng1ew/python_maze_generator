"""Точка входа в программу A1_Maze_Py.

Запуск:
    python -m src.main
"""

from src.maze.gui import run_app


def main() -> None:
    """Запускает GUI-приложение."""
    run_app()


if __name__ == "__main__":
    # Эта проверка — питоновский аналог `int main(void)` в Си.
    # Код внутри выполняется только если файл запущен напрямую,
    # а не импортирован как модуль.
    main()
