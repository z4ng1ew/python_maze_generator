import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from generator.path_generator import PathGenerator

def test_heuristic():
    pg = PathGenerator(
        ((0, 0), (3, 4)),
        [[1]],
        [[1]]
    )

    assert pg.heuristic(0, 0) == 7

def test_neighbors_right_open():
    right = [
        [0, 1]
    ]

    bottom = [
        [1, 1]
    ]

    pg = PathGenerator(
        ((0, 0), (1, 0)),
        right,
        bottom
    )

    assert (1, 0) in pg.get_neighbors(0, 0)

def test_neighbors_bottom_open():
    right = [
        [1],
        [1]
    ]

    bottom = [
        [0],
        [1]
    ]

    pg = PathGenerator(
        ((0, 0), (0, 1)),
        right,
        bottom
    )

    assert (0, 1) in pg.get_neighbors(0, 0)

def test_search_path_simple():
    right = [
        [0, 1]
    ]

    bottom = [
        [1, 1]
    ]

    pg = PathGenerator(
        ((0, 0), (1, 0)),
        right,
        bottom
    )

    path = pg.search_path()

    assert path == [
        (0, 0),
        (1, 0)
    ]

def test_search_path_not_found():
    right = [
        [1, 1]
    ]

    bottom = [
        [1, 1]
    ]

    pg = PathGenerator(
        ((0, 0), (1, 0)),
        right,
        bottom
    )

    assert pg.search_path() is None

def test_search_path_same_point():
    pg = PathGenerator(
        ((0, 0), (0, 0)),
        [[1]],
        [[1]]
    )

    assert pg.search_path() == [(0, 0)]

def test_search_path_none_points():
    pg = PathGenerator(
        (None, (0, 0)),
        [[1]],
        [[1]]
    )

    assert pg.search_path() is None

def test_neighbors_left_open():
    right = [[0, 1]]
    bottom = [[1, 1]]

    pg = PathGenerator(
        ((1, 0), (0, 0)),
        right,
        bottom
    )

    assert (0, 0) in pg.get_neighbors(1, 0)

def test_neighbors_up_open():
    right = [
        [1],
        [1]
    ]

    bottom = [
        [0],
        [1]
    ]

    pg = PathGenerator(
        ((0, 1), (0, 0)),
        right,
        bottom
    )

    assert (0, 0) in pg.get_neighbors(0, 1)


def test_path_starts_and_ends_correctly():
    right = [[0, 1]]
    bottom = [[1, 1]]

    pg = PathGenerator(
        ((0, 0), (1, 0)),
        right,
        bottom
    )

    path = pg.search_path()

    assert path[0] == (0, 0)
    assert path[-1] == (1, 0)