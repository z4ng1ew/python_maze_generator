from modules.algorithm import bfs, get_path, is_perfect_maze
from modules.maze import Maze


def test_find_path(maze1: Maze) -> None:
    frm: list[list[tuple[int, int]]] = bfs(maze1, (0, 0))
    path: list[tuple[int, int]] = get_path(frm, (2, 2))
    assert path == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]


def test_is_perfect_maze(maze1: Maze) -> None:
    frm: list[list[tuple[int, int]]] = bfs(maze1, (0, 0))
    assert is_perfect_maze(frm)


def test_is_not_perfect_maze(maze1: Maze) -> None:
    frm: list[list[tuple[int, int]]] = bfs(maze1, (0, 0))
    frm[8][8] = (-1, -1)
    assert not is_perfect_maze(frm)
