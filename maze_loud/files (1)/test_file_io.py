"""Модульные тесты для src.maze.file_io."""

import pytest
from pathlib import Path

from src.maze.domain import Maze, DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP
from src.maze.file_io import load_maze, save_maze, MazeFileError


# ==== Загрузка из файла ====


def test_load_example_4x4(tmp_path: Path) -> None:
    """Файл 4x4 из задания должен парситься без ошибок.

    tmp_path — встроенный pytest-fixture (временная папка),
    она удаляется после теста автоматически.
    """
    content = (
        "4 4\n"
        "0 0 0 1\n"
        "1 0 1 1\n"
        "0 1 0 1\n"
        "0 0 0 1\n"
        "\n"
        "1 0 1 0\n"
        "0 0 1 0\n"
        "1 1 0 1\n"
        "1 1 1 1\n"
    )
    path = tmp_path / "maze.txt"
    path.write_text(content)

    maze = load_maze(path)

    assert maze.rows == 4
    assert maze.cols == 4
    assert maze.vertical_walls[0] == [0, 0, 0, 1]
    assert maze.horizontal_walls[3] == [1, 1, 1, 1]


def test_load_minimal_1x1(tmp_path: Path) -> None:
    content = "1 1\n1\n\n1\n"
    path = tmp_path / "m.txt"
    path.write_text(content)

    maze = load_maze(path)

    assert maze.rows == 1
    assert maze.cols == 1


def test_load_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        load_maze("/nonexistent/path.txt")


def test_load_empty_file_raises(tmp_path: Path) -> None:
    path = tmp_path / "empty.txt"
    path.write_text("")
    with pytest.raises(MazeFileError):
        load_maze(path)


def test_load_bad_dimensions_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.txt"
    path.write_text("abc def\n")
    with pytest.raises(MazeFileError):
        load_maze(path)


def test_load_too_short_raises(tmp_path: Path) -> None:
    path = tmp_path / "short.txt"
    path.write_text("4 4\n0 0 0 1\n")
    with pytest.raises(MazeFileError):
        load_maze(path)


def test_load_bad_value_raises(tmp_path: Path) -> None:
    """Числа в матрице должны быть 0 или 1."""
    content = (
        "2 2\n"
        "0 1\n"
        "0 5\n"  # 5 — недопустимо
        "\n"
        "0 0\n"
        "1 1\n"
    )
    path = tmp_path / "bad.txt"
    path.write_text(content)
    with pytest.raises(MazeFileError):
        load_maze(path)


def test_load_wrong_columns_count(tmp_path: Path) -> None:
    content = (
        "2 3\n"
        "0 1 0\n"
        "0 1\n"  # только 2 числа вместо 3
        "\n"
        "0 0 1\n"
        "1 1 1\n"
    )
    path = tmp_path / "bad.txt"
    path.write_text(content)
    with pytest.raises(MazeFileError):
        load_maze(path)


# ==== Сохранение в файл ====


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    """То, что сохранили, должны прочитать обратно без потерь."""
    original = Maze(
        rows=2,
        cols=2,
        vertical_walls=[[1, 1], [0, 1]],
        horizontal_walls=[[0, 1], [1, 1]],
    )
    path = tmp_path / "rt.txt"

    save_maze(original, path)
    loaded = load_maze(path)

    assert loaded.rows == original.rows
    assert loaded.cols == original.cols
    assert loaded.vertical_walls == original.vertical_walls
    assert loaded.horizontal_walls == original.horizontal_walls


# ==== Методы класса Maze ====


def test_maze_external_walls_default() -> None:
    """Если матрицы не переданы, внешние стены должны быть выставлены."""
    maze = Maze(rows=3, cols=3)
    # правая внешняя стена
    for r in range(3):
        assert maze.vertical_walls[r][2] == 1
    # нижняя внешняя стена
    for c in range(3):
        assert maze.horizontal_walls[2][c] == 1


def test_maze_invalid_size_raises() -> None:
    with pytest.raises(ValueError):
        Maze(rows=0, cols=5)
    with pytest.raises(ValueError):
        Maze(rows=51, cols=5)


def test_has_wall_directions() -> None:
    """Проверяем все 4 направления."""
    # 2x2: разделяющая стена справа от (0,0), снизу от (0,0)
    maze = Maze(
        rows=2,
        cols=2,
        vertical_walls=[[1, 1], [0, 1]],
        horizontal_walls=[[1, 0], [1, 1]],
    )
    assert maze.has_wall((0, 0), DIR_RIGHT) is True
    assert maze.has_wall((0, 0), DIR_DOWN) is True
    assert maze.has_wall((0, 0), DIR_LEFT) is True   # внешняя
    assert maze.has_wall((0, 0), DIR_UP) is True     # внешняя

    # У (1, 0) сверху стена есть (horizontal_walls[0][0] == 1)
    assert maze.has_wall((1, 0), DIR_UP) is True
    # У (1, 1) слева стены нет (vertical_walls[1][0] == 0)
    assert maze.has_wall((1, 1), DIR_LEFT) is False


def test_neighbors_returns_only_reachable() -> None:
    # Открытый лабиринт 2x2 (только внешние стены)
    maze = Maze(rows=2, cols=2)
    # (0, 0) — должны быть достижимы (0, 1) и (1, 0)
    nbrs = sorted(maze.neighbors((0, 0)))
    assert nbrs == [(0, 1), (1, 0)]
