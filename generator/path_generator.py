import heapq

class PathGenerator:
    def __init__(self, start_end_states, right_walls, bottom_walls):
        self.start = start_end_states[0]
        self.end = start_end_states[1]
        self.right_walls = right_walls
        self.bottom_walls = bottom_walls
        self.height = len(right_walls)
        self.width = len(right_walls[0])

    def heuristic(self, x, y):

        ex, ey = self.end
        return abs(x - ex) + abs(y - ey)

    def get_neighbors(self, x, y):
        neighbors = []
        if x < self.width - 1 and self.right_walls[y][x] == 0:
            neighbors.append((x + 1, y))

        if x > 0 and self.right_walls[y][x - 1] == 0:
            neighbors.append((x - 1, y))

        if y < self.height - 1 and self.bottom_walls[y][x] == 0:
            neighbors.append((x, y + 1))
            
        if y > 0 and self.bottom_walls[y - 1][x] == 0:
            neighbors.append((x, y - 1))
        return neighbors

    def search_path(self):
        if self.start is None or self.end is None:
            return None
        sx, sy = self.start

        open_heap = [(self.heuristic(sx, sy), 0, self.start)]
        g_score = {self.start: 0}
        parent = {}

        while open_heap:
            f, g, current = heapq.heappop(open_heap)

            if current == self.end:
                break

            if g > g_score.get(current, float('inf')):
                continue

            x, y = current
            for neighbor in self.get_neighbors(x, y):
                tentative_g = g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    nx, ny = neighbor
                    f_new = tentative_g + self.heuristic(nx, ny)
                    parent[neighbor] = current
                    heapq.heappush(open_heap, (f_new, tentative_g, neighbor))

        if self.end not in g_score:
            return None

        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = parent[current]
        path.append(self.start)
        path.reverse()
        return path