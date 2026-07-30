from pathlib import Path

class MazeLoader():
    """загрузка лабиринта"""
    def __init__(self):
        pass
    
    def load(self, filename):
        return read_maze_from_file(Path(f'./dataSorce/save_mazes/{filename}'))

        
def read_matrix(size, f):
    matrix = []
    for _ in range(size):
        line = list(map(int, f.readline().split()))
        matrix.append(line)
    return matrix


def read_maze_from_file(file_path):  
    with open(file_path, 'r') as f:
        size = int(f.readline().split()[0])

        matrix_1 = read_matrix(size, f)
        f.readline()
        matrix_2 = read_matrix(size, f)
    return size, matrix_1, matrix_2



