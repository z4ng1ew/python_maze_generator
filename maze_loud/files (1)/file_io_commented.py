"""Загрузка и сохранение лабиринта в текстовом формате.

Формат файла:
    rows cols
    <матрица вертикальных стен: rows строк по cols чисел>
    <пустая строка>
    <матрица горизонтальных стен: rows строк по cols чисел>

Каждое число — 0 или 1 (нет/есть стена).
"""

from pathlib import Path
# pathlib — современный модуль для работы с путями. Заменяет os.path.
# Path("a") / "b" → "a/b" (с правильным разделителем для ОС).
# Аналогия: как std::filesystem::path в C++17.

from typing import List, Tuple

from src.maze.domain import Maze, Matrix
# Импорт через src.maze.domain — это абсолютный импорт от корня проекта.
# Чтобы он работал, программу запускают как `python -m src.main` из корня.


# Тип, который возвращает парсер: либо Maze, либо ничего (если ошибка)
ParsedMaze = Maze


class MazeFileError(ValueError):
    """Своё исключение для ошибок формата файла.

    Зачем своё? Чтобы в GUI можно было поймать именно ЭТО исключение
    и показать понятное сообщение, а не падать на любом ValueError.
    Аналог: разные коды ошибок (errno) в Си, но через типы.
    """


def load_maze(path: str | Path) -> Maze:
    """Читает лабиринт из файла.

    Args:
        path: путь к файлу (строка или объект Path).

    Returns:
        Объект Maze, готовый к отрисовке.

    Raises:
        MazeFileError: если формат файла нарушен.
        FileNotFoundError: если файла нет (стандартное Python-исключение).

    Алгоритм:
      1. Открываем файл, читаем все строки.
      2. Убираем пустые строки (которые нужны как разделитель,
         но при разборе они не несут данных — мы и так знаем,
         сколько строк должно быть в каждой матрице).
      3. Первая строка — размеры (rows cols).
      4. Следующие rows строк — вертикальные стены.
      5. Следующие rows строк — горизонтальные стены.
    """
    path = Path(path)
    # читаем весь файл в строку и режем по строкам
    text = path.read_text(encoding="utf-8")
    # split() без аргументов режет по любым пробельным символам и
    # выкидывает пустые элементы — нам нужно поведение тоньше,
    # поэтому режем по \n и сами фильтруем.
    raw_lines = [line.strip() for line in text.splitlines()]
    # фильтруем пустые строки
    lines = [line for line in raw_lines if line]

    if len(lines) < 1:
        raise MazeFileError("Файл пустой")

    # Парсим первую строку: размеры
    try:
        rows, cols = (int(x) for x in lines[0].split())
    except ValueError as exc:
        raise MazeFileError(
            f"Первая строка должна быть 'rows cols', получено: {lines[0]!r}"
        ) from exc
    # 'from exc' — связывает наше исключение с первоначальным.
    # При падении в трейсбэке (traceback — стек вызовов при ошибке)
    # будут видны обе причины. Полезно для отладки.

    expected_total = 1 + rows + rows  # размер + 2 матрицы по rows строк
    if len(lines) < expected_total:
        raise MazeFileError(
            f"Ожидалось {expected_total} непустых строк, получено {len(lines)}"
        )

    # Срезы списков (slices): lines[1:1+rows] — это элементы с 1 по 1+rows-1.
    # Аналог: цикл for i = 1; i < 1+rows; i++ в Си.
    vert_lines = lines[1 : 1 + rows]
    horiz_lines = lines[1 + rows : 1 + 2 * rows]

    vertical_walls = _parse_matrix(vert_lines, rows, cols, "вертикальных стен")
    horizontal_walls = _parse_matrix(
        horiz_lines, rows, cols, "горизонтальных стен"
    )

    # Создание объекта Maze. Если данные невалидны — Maze.__post_init__
    # сам выбросит ValueError. Мы перепаковываем его в наш MazeFileError.
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
    """Превращает список строк в матрицу 0/1.

    Внутренняя функция (приватная — отсюда подчёркивание в начале).
    Используется только внутри этого модуля.
    """
    matrix: Matrix = []
    for r, line in enumerate(lines):
        # enumerate(lines) даёт пары (индекс, элемент).
        # Аналог: for (int r = 0; r < n; r++) line = lines[r];
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
    """Сохраняет лабиринт в файл в том же формате, что читает load_maze.

    Это понадобится в Части 2 — после генерации лабиринт нужно
    сохранять в файл.
    """
    path = Path(path)
    parts: List[str] = [f"{maze.rows} {maze.cols}"]

    # Вертикальные стены
    for row in maze.vertical_walls:
        parts.append(" ".join(str(v) for v in row))

    # Пустая строка-разделитель — для совместимости с примером в задании
    parts.append("")

    # Горизонтальные стены
    for row in maze.horizontal_walls:
        parts.append(" ".join(str(v) for v in row))

    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
