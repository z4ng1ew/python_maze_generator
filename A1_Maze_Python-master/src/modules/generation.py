import random

from modules.maze import Cell, Maze

CLOSED_WALLS = {
    'top': True,
    'left': True,
    'right': True,
    'bottom': True,
}


class State:
    def __init__(self, width: int, y: int = 0, next_set: int = -1) -> None:
        self.width = width
        self.y = y
        self.next_set = next_set
        self.cells: list[Cell] = [Cell(x, y, CLOSED_WALLS) for x in range(width)]
        self.sets: dict[int, list[Cell]] = {}

    def populate(self) -> None:
        """Назначение уникальных множеств всем клеткам в текущей строке."""
        for cell in self.cells:
            if cell.set_id == 0:
                self.next_set += 1
                cell.set_id = self.next_set
                self.sets[self.next_set] = [cell]
        return self

    def next(self) -> None:
        """Создание следующей строки на основе текущей."""
        new_state = State(self.width, self.y + 1, self.next_set)
        new_state.cells = [
            Cell(cell.x, self.y + 1, CLOSED_WALLS) for cell in self.cells
        ]
        return new_state

    def merge(self, sink_cell: Cell, target_cell: Cell) -> None:
        """Объединение двух множеств."""
        sink_set, target_set = sink_cell.set_id, target_cell.set_id
        if sink_set == target_set:
            return

        for cell in self.sets[target_set]:
            cell.set_id = sink_set
            self.sets[sink_set].append(cell)

        del self.sets[target_set]

    def same(self, a: Cell, b: Cell) -> bool:
        """Проверка принадлежности клеток одному множеству."""
        return a.set_id == b.set_id

    def add_to_set(self, cell: Cell, set_id: int) -> None:
        """Добавление клетки в множество."""
        cell.set_id = set_id
        if set_id not in self.sets:
            self.sets[set_id] = []
        self.sets[set_id].append(cell)


class MazeEller(Maze):
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.field: list[list[Cell]] = [
            [Cell(col, row, CLOSED_WALLS) for col in range(cols)] for row in range(rows)
        ]

    @staticmethod
    def step(state: State, finish: bool = False) -> None:
        """Основной шаг алгоритма Эллера."""
        # Создание горизонтальных проходов
        for i in range(state.width - 1):
            current_cell = state.cells[i]
            next_cell = state.cells[i + 1]

            if not state.same(current_cell, next_cell) and (
                finish or random.choice([True, False])
            ):
                current_cell.walls['right'] = False
                next_cell.walls['left'] = False
                state.merge(current_cell, next_cell)

        # Создание вертикальных проходов
        verticals = []
        next_state = state.next()

        if finish:
            return next_state.populate(), state.cells

        for set_cells in state.sets.values():
            # Выбираем случайные клетки из множества для вертикального соединения
            cells_to_connect = random.sample(
                set_cells, max(1, random.randint(1, len(set_cells)))
            )
            for cell in cells_to_connect:
                verticals.append(cell)
                next_cell = next_state.cells[cell.x]
                next_cell.walls['top'] = False
                cell.walls['bottom'] = False
                next_state.add_to_set(next_cell, cell.set_id)

        return next_state.populate(), state.cells

    def generate(self) -> None:
        """Генерация лабиринта с помощью алгоритма Эллера."""
        state = State(self.cols).populate()

        finish = False
        for row in range(self.rows):
            if row == self.rows - 1:
                finish = True
            state, cells = self.step(state, finish=finish)
            self.field[row] = cells
