from collections import deque

from modules.exception import BaseMazeException
from modules.maze import Cell, Maze


def bfs(maze: Maze, s: tuple[int, int]) -> list[list[tuple[int, int]]]:
    """

    Args:
        maze (Maze): лабиринт
        s (tuple): начальная точка

    Returns:
        list[list[tuple[int, int]]]: Матрица, в которой у каждой точки записана точка, из которой в неё пришли.
    """

    INF: int = 10**9
    dist: list[list[int]] = [[INF] * maze.cols for _ in range(maze.rows)]
    frm: list[list[tuple[int, int]]] = [
        [(-1, -1)] * maze.cols for _ in range(maze.rows)
    ]
    q: deque[Cell] = deque()
    dist[s[1]][s[0]] = 0
    q.append(maze.field[s[1]][s[0]])

    while q:
        v: Cell = q.pop()
        for side, have_wall in v.walls.items():
            if not have_wall:
                to: Cell
                if side == 'top':
                    to = maze.field[v.y - 1][v.x]
                elif side == 'bottom':
                    to = maze.field[v.y + 1][v.x]
                elif side == 'left':
                    to = maze.field[v.y][v.x - 1]
                elif side == 'right':
                    to = maze.field[v.y][v.x + 1]
                if dist[to.y][to.x] == INF:
                    dist[to.y][to.x] = dist[v.y][v.x] + 1
                    frm[to.y][to.x] = (v.x, v.y)
                    q.append(to)
    return frm


def get_path(
    frm: list[list[tuple[int, int]]], f: tuple[int, int]
) -> list[tuple[int, int]]:
    """

    Args:
        frm (list[list[tuple[int, int]]]): Матрица путей в каждую точку
        f (tuple[int, int]): Конечная точка

    Returns:
        list[tuple[int, int]]: Восстановленный путь
    """
    if f[0] >= len(frm[0]) or f[1] >= len(frm):
        raise BaseMazeException('End point out of range')
    v: tuple[int, int] = f
    path: list[tuple[int, int]] = []
    while v != (-1, -1):
        path.append(v)
        v = frm[v[1]][v[0]]
    path.reverse()
    return path


def is_perfect_maze(frm: list[list[tuple[int, int]]]) -> bool:
    return sum([row.count((-1, -1)) for row in frm]) <= 1
