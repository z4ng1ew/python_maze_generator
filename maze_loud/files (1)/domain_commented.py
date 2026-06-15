"""Доменная модель лабиринта.

Лабиринт хранится как:
  - размеры (rows, cols)
  - матрица вертикальных стен (стена справа от ячейки)
  - матрица горизонтальных стен (стена снизу от ячейки)

Соглашение: 1 = стена есть, 0 = стены нет.

Аналогия для тех, кто из Си:
  Это как struct Maze {
      int rows, cols;
      int **vert;   // [rows][cols]
      int **horiz;  // [rows][cols]
  };
  плюс набор функций, работающих с указателем на этот struct.
  В Python мы оборачиваем поля в class и методы — суть та же.
"""

from dataclasses import dataclass, field
# dataclass — декоратор, который автоматически генерирует
# конструктор __init__, метод сравнения __eq__ и __repr__ для строкового
# представления. Это как макрос в Си, экономит ручную писанину.

from typing import List, Tuple
# typing — модуль с подсказками типов (type hints).
# Они не проверяются на ран-тайме, но помогают редактору и pylint/mypy
# ловить ошибки. Аналог объявления типов в Си, но необязательный.

# Псевдонимы типов — чтобы код читался как текст
Matrix = List[List[int]]   # двумерный список целых
Point = Tuple[int, int]    # координата (row, col)


# Константы направлений. Использую enum-подобный подход через целые,
# чтобы было привычно для Си-разработчика.
DIR_RIGHT = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_UP = 3


@dataclass
class Maze:
    """Лабиринт с тонкими стенами.

    Атрибуты:
        rows: число строк (1..50 по требованиям задания).
        cols: число столбцов (1..50).
        vertical_walls: матрица rows x cols. vertical_walls[r][c] == 1,
            если справа от ячейки (r, c) стоит стена.
            Последний столбец (c == cols - 1) — это правая внешняя стена,
            всегда == 1.
        horizontal_walls: матрица rows x cols. horizontal_walls[r][c] == 1,
            если снизу от ячейки (r, c) стоит стена.
            Последняя строка (r == rows - 1) — это нижняя внешняя стена,
            всегда == 1.
    """

    rows: int
    cols: int
    # field(default_factory=list) — это безопасный способ задать
    # пустой список как значение по умолчанию. Если просто написать = [],
    # то ВСЕ объекты класса будут делить ОДИН и тот же список (общая
    # известная ловушка Python). default_factory вызывает list() для
    # каждого нового объекта.
    vertical_walls: Matrix = field(default_factory=list)
    horizontal_walls: Matrix = field(default_factory=list)

    def __post_init__(self) -> None:
        """Вызывается после автогенерируемого __init__.

        Здесь делаем валидацию и, если нужно, заполняем стенами по умолчанию.
        Аналогия: ассерты после аллокации struct в Си.
        """
        if not 1 <= self.rows <= 50:
            raise ValueError(f"rows должно быть 1..50, получено {self.rows}")
        if not 1 <= self.cols <= 50:
            raise ValueError(f"cols должно быть 1..50, получено {self.cols}")

        # Если матрицы стен не переданы — создаём пустые (все нули).
        # Внешние стены (правый край и нижний край) ставим в 1.
        if not self.vertical_walls:
            self.vertical_walls = [[0] * self.cols for _ in range(self.rows)]
            # Правая внешняя стена
            for r in range(self.rows):
                self.vertical_walls[r][self.cols - 1] = 1

        if not self.horizontal_walls:
            self.horizontal_walls = [[0] * self.cols for _ in range(self.rows)]
            # Нижняя внешняя стена
            for c in range(self.cols):
                self.horizontal_walls[self.rows - 1][c] = 1

        self._validate_dimensions()

    def _validate_dimensions(self) -> None:
        """Проверяет, что размеры матриц соответствуют rows x cols.

        Подчёркивание перед именем — соглашение Python: "это приватный метод,
        снаружи класса лучше не трогать". Жёстко не запрещено (в Си нет
        такого вообще), но это договорённость сообщества.
        """
        if len(self.vertical_walls) != self.rows:
            raise ValueError("vertical_walls: неверное число строк")
        if len(self.horizontal_walls) != self.rows:
            raise ValueError("horizontal_walls: неверное число строк")
        for r in range(self.rows):
            if len(self.vertical_walls[r]) != self.cols:
                raise ValueError(f"vertical_walls[{r}]: неверная длина строки")
            if len(self.horizontal_walls[r]) != self.cols:
                raise ValueError(
                    f"horizontal_walls[{r}]: неверная длина строки"
                )

    def has_wall(self, point: Point, direction: int) -> bool:
        """Есть ли стена у ячейки `point` в направлении `direction`.

        Args:
            point: (row, col) — координата ячейки.
            direction: одна из констант DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP.

        Returns:
            True, если в этом направлении стена.

        Логика:
          - DIR_RIGHT: стена справа от (r, c) — это vertical_walls[r][c].
          - DIR_DOWN: стена снизу от (r, c) — это horizontal_walls[r][c].
          - DIR_LEFT: это стена СПРАВА от (r, c-1), то есть
                      vertical_walls[r][c-1]. Если c == 0 — мы у левой
                      внешней стены, она всегда есть.
          - DIR_UP: симметрично — horizontal_walls[r-1][c],
                    или 1 если r == 0.
        """
        r, c = point
        if direction == DIR_RIGHT:
            return self.vertical_walls[r][c] == 1
        if direction == DIR_DOWN:
            return self.horizontal_walls[r][c] == 1
        if direction == DIR_LEFT:
            if c == 0:
                return True
            return self.vertical_walls[r][c - 1] == 1
        if direction == DIR_UP:
            if r == 0:
                return True
            return self.horizontal_walls[r - 1][c] == 1
        raise ValueError(f"Неизвестное направление: {direction}")

    def neighbors(self, point: Point) -> List[Point]:
        """Возвращает соседние ячейки, до которых можно дойти (без стены).

        Это понадобится для поиска пути (Часть 3).
        Алгоритм: для каждого из 4 направлений проверяем стену; если её нет
        и соседняя клетка внутри сетки — добавляем в список.
        """
        r, c = point
        # Карта направлений: (dr, dc, direction_const)
        moves = (
            (0, 1, DIR_RIGHT),
            (1, 0, DIR_DOWN),
            (0, -1, DIR_LEFT),
            (-1, 0, DIR_UP),
        )
        result: List[Point] = []
        for dr, dc, direction in moves:
            if self.has_wall((r, c), direction):
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                result.append((nr, nc))
        return result
