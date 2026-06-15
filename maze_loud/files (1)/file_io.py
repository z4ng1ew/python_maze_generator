"""Загрузка и сохранение лабиринта в текстовом формате."""

from pathlib import Path
from typing import List

from src.maze.domain import Maze, Matrix


class MazeFileError(ValueError):
    """Ошибка формата файла лабиринта."""


def load_maze(path: str | Path) -> Maze:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    raw_lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in raw_lines if line]

    if len(lines) < 1:
        raise MazeFileError("Файл пустой")

    try:
        rows, cols = (int(x) for x in lines[0].split())
    except ValueError as exc:
        raise MazeFileError(
            f"Первая строка должна быть 'rows cols', получено: {lines[0]!r}"
        ) from exc

    expected_total = 1 + rows + rows
    if len(lines) < expected_total:
        raise MazeFileError(
            f"Ожидалось {expected_total} непустых строк, получено {len(lines)}"
        )

    vert_lines = lines[1 : 1 + rows]
    horiz_lines = lines[1 + rows : 1 + 2 * rows]

    vertical_walls = _parse_matrix(vert_lines, rows, cols, "вертикальных стен")
    horizontal_walls = _parse_matrix(
        horiz_lines, rows, cols, "горизонтальных стен"
    )

    try:
        return Maze(
            rows=rows,
            cols=cols,
            vertical_walls=vertical_walls,
            horizontal_walls=horizontal_walls,
        )
    except ValueError as exc:
        raise MazeFileError(str(exc)) from exc


def _parse_matrix(
    lines: List[str],
    rows: int,
    cols: int,
    name: str,
) -> Matrix:
    matrix: Matrix = []
    for r, line in enumerate(lines):
        values = line.split()
        if len(values) != cols:
            raise MazeFileError(
                f"Матрица {name}: строка {r}: ожидалось {cols} чисел, "
                f"получено {len(values)}"
            )
        try:
            row = [int(v) for v in values]
        except ValueError as exc:
            raise MazeFileError(
                f"Матрица {name}: строка {r}: не число: {line!r}"
            ) from exc
        for c, val in enumerate(row):
            if val not in (0, 1):
                raise MazeFileError(
                    f"Матрица {name}: ({r}, {c}) = {val}, должно быть 0 или 1"
                )
        matrix.append(row)
    return matrix


def save_maze(maze: Maze, path: str | Path) -> None:
    path = Path(path)
    parts: List[str] = [f"{maze.rows} {maze.cols}"]

    for row in maze.vertical_walls:
        parts.append(" ".join(str(v) for v in row))

    parts.append("")

    for row in maze.horizontal_walls:
        parts.append(" ".join(str(v) for v in row))

    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
