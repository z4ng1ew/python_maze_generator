from modules.algorithm import bfs, is_perfect_maze
from modules.exception import BaseMazeException
from modules.maze import Maze


class Loader:
    def __init__(self, maze: Maze | None = None) -> None:
        self.maze = maze

    def download(self, file: str) -> Maze:
        # Считывание всего файла
        try:
            with open(file, 'r') as f:
                maze_data = [list(map(int, line.split())) for line in f]
            # Создание пустого лабиринта
            rows, cols = maze_data[0]
            self.maze = Maze(rows, cols)
        except Exception as err:
            raise BaseMazeException(f'Incorrect file [{file}]: {err}') from err
        # Заполнение правых и левых стенок из 1 матрицы
        for row in range(rows):
            for col in range(cols):
                i = row + 1
                if maze_data[i][col] == 1:
                    self.maze.field[row][col].walls['right'] = True
                    if col < cols - 1:
                        self.maze.field[row][col + 1].walls['left'] = True
        # Заполнение нижних и верхних стенок из 2 матрицы
        for row in range(rows):
            for col in range(cols):
                i = row + rows + 2
                if maze_data[i][col] == 1:
                    self.maze.field[row][col].walls['bottom'] = True
                    if row < rows - 1:
                        self.maze.field[row + 1][col].walls['top'] = True
        # Заполнение верхней и левой стенки лабиринта
        for row in range(rows):
            self.maze.field[row][0].walls['left'] = True
        for col in range(cols):
            self.maze.field[0][col].walls['top'] = True

        if not is_perfect_maze(bfs(self.maze, (0, 0))):
            raise BaseMazeException('Invalid maze')
        return self.maze

    def upload(self, file: str, maze: Maze) -> None:
        if maze:
            with open(file, 'w') as f:
                f.write(' '.join(list(map(str, [maze.rows, maze.cols]))) + '\n')
                for row in maze.field:
                    f.write(
                        ' '.join(list(map(str, [int(i.walls['right']) for i in row])))
                        + '\n'
                    )
                f.write('\n')
                for row in maze.field:
                    f.write(
                        ' '.join(list(map(str, [int(i.walls['bottom']) for i in row])))
                        + '\n'
                    )
