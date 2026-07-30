import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from generator.generator import MazeGenerator

from generator.generator import (
    set_right_walls,
    set_bottom_walls,
    next_row,
    MazeGenerator,
)

def test_next_row_creates_new_sets_for_closed_bottoms():
    prev_bottom = [1, 0, 1]
    prev_row = [1, 2, 3]

    row, counter = next_row(
        size=3,
        prev_bottom=prev_bottom,
        prev_row=prev_row,
        counter=4
    )

    assert row == [4, 2, 5]
    assert counter == 6


def test_next_row_keeps_open_cells():
    prev_bottom = [0, 0, 0]
    prev_row = [1, 2, 3]

    row, counter = next_row(3, prev_bottom, prev_row, 4)

    assert row == [1, 2, 3]
    assert counter == 4


def test_set_right_walls_last_row():
    row = [1, 2, 3]
    right = [1, 1, 1]

    set_right_walls(
        size=3,
        right_walls_row=right,
        row=row,
        last=True
    )

    assert right == [0, 0, 1]
    assert len(set(row)) == 1


def test_set_bottom_walls_every_group_has_exit(monkeypatch):
    def always_one(a, b):
        return 1

    monkeypatch.setattr("random.randint", always_one)

    row = [1, 1, 2, 2]
    bottom = [0, 0, 0, 0]

    set_bottom_walls(4, bottom, row)

    groups = {
        1: [0, 1],
        2: [2, 3]
    }

    for cells in groups.values():
        assert any(bottom[i] == 0 for i in cells)


def test_create_maze_size_5():
    generator = MazeGenerator()

    right, bottom = generator.create_maze(5)

    assert len(right) == 5
    assert len(bottom) == 5

    for row in right:
        assert len(row) == 5

    for row in bottom:
        assert len(row) == 5


def test_last_row_bottom_walls_closed():
    generator = MazeGenerator()

    _, bottom = generator.create_maze(5)

    assert bottom[-1] == [1, 1, 1, 1, 1]


def test_last_row_right_wall_closed():
    generator = MazeGenerator()

    right, _ = generator.create_maze(5)

    assert right[-1][-1] == 1




from collections import deque


def get_neighbors(x, y, right, bottom):
    h = len(right)
    w = len(right[0])

    result = []

    if x < w - 1 and right[y][x] == 0:
        result.append((x + 1, y))

    if x > 0 and right[y][x - 1] == 0:
        result.append((x - 1, y))

    if y < h - 1 and bottom[y][x] == 0:
        result.append((x, y + 1))

    if y > 0 and bottom[y - 1][x] == 0:
        result.append((x, y - 1))

    return result


def test_maze_is_connected():
    gen = MazeGenerator()

    right, bottom = gen.create_maze(10)

    visited = set()
    queue = deque([(0, 0)])

    while queue:
        cell = queue.popleft()

        if cell in visited:
            continue

        visited.add(cell)

        for n in get_neighbors(*cell, right, bottom):
            queue.append(n)

    assert len(visited) == 100


def test_maze_has_no_cycles():
    gen = MazeGenerator()

    right, bottom = gen.create_maze(10)

    vertices = 100
    edges = 0

    for y in range(10):
        for x in range(10):

            if x < 9 and right[y][x] == 0:
                edges += 1

            if y < 9 and bottom[y][x] == 0:
                edges += 1

    assert edges == vertices - 1

def test_create_maze_size_1():
    gen = MazeGenerator()

    right, bottom = gen.create_maze(1)

    assert right == [[1]]
    assert bottom == [[1]]

