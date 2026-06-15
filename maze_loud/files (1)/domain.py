"""Доменная модель лабиринта."""

from dataclasses import dataclass, field
from typing import List, Tuple

Matrix = List[List[int]]
Point = Tuple[int, int]

DIR_RIGHT = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_UP = 3


@dataclass
class Maze:
    """Лабиринт с тонкими стенами."""

    rows: int
    cols: int
    vertical_walls: Matrix = field(default_factory=list)
    horizontal_walls: Matrix = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 1 <= self.rows <= 50:
            raise ValueError(f"rows должно быть 1..50, получено {self.rows}")
        if not 1 <= self.cols <= 50:
            raise ValueError(f"cols должно быть 1..50, получено {self.cols}")

        if not self.vertical_walls:
            self.vertical_walls = [[0] * self.cols for _ in range(self.rows)]
            for r in range(self.rows):
                self.vertical_walls[r][self.cols - 1] = 1

        if not self.horizontal_walls:
            self.horizontal_walls = [[0] * self.cols for _ in range(self.rows)]
            for c in range(self.cols):
                self.horizontal_walls[self.rows - 1][c] = 1

        self._validate_dimensions()

    def _validate_dimensions(self) -> None:
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
        r, c = point
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
