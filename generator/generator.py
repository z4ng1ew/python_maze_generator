import random

def set_right_walls(size, right_walls_row, row, last=False):
    if last:
        for i in range(size - 1):
            if row[i] != row[i + 1]:
                right_walls_row[i] = 0
                old = row[i + 1]          
                for k in range(size):
                    if row[k] == old:
                        row[k] = row[i]
            else:
                right_walls_row[i] = 1
            print("Last row sets:", row)
        right_walls_row[size - 1] = 1
    else:
        for j in range(size - 1):
            if row[j] == row[j + 1] or random.randint(0, 1):
                right_walls_row[j] = 1
            else:
                right_walls_row[j] = 0
                old = row[j + 1]          
                for k in range(size):
                    if row[k] == old:
                        row[k] = row[j]
        right_walls_row[size - 1] = 1

def set_bottom_walls(size, bottom_walls_row, row):
    groups = {}
    for j in range(size):
        groups.setdefault(row[j], []).append(j)

    for cells in groups.values():
        opened = [idx for idx in cells if not random.randint(0, 1)]
        if not opened:
            opened = [random.choice(cells)]
        for idx in cells:
            bottom_walls_row[idx] = 0 if idx in opened else 1


            
def next_row(size, prev_bottom, prev_row, counter):
    row = prev_row.copy()
    for j in range(size):
        if prev_bottom[j]:
            row[j] = counter
            counter += 1
    return row, counter


class MazeGenerator:
    def create_maze(self, size):
        counter = size + 1
        row = list(range(1, size + 1))

        right_walls  = [[0] * size for _ in range(size)]
        bottom_walls = [[0] * size for _ in range(size)]


        set_right_walls(size, right_walls[0], row)
        set_bottom_walls(size, bottom_walls[0], row)


        for i in range(1, size - 1):
            row, counter = next_row(size, bottom_walls[i - 1], row, counter)
            set_right_walls(size, right_walls[i], row)
            set_bottom_walls(size, bottom_walls[i], row)


        row, _ = next_row(size, bottom_walls[size - 2], row, counter)
        bottom_walls[size - 1] = [1] * size
        set_right_walls(size, right_walls[size - 1], row, last=True)

        return right_walls, bottom_walls