import customtkinter as ctk
from generator.generator import MazeGenerator
from dataSorce.maze_loader import MazeLoader
from dataSorce.maze_save import MazeSave
from generator.path_generator import PathGenerator

BG          = "#0F172A"
WALL        = "#CBD5E1"
CELL_START  = "#6366F1"
CELL_END    = "#EC4899"
CELL_PATH   = "#22D3EE"   


class RenderMaze:
    def __init__(self, app, root, size, file):
        self.app  = app
        self.root = root
        self.size = size
        self.file = file

        self.canvas     = None
        self.cell       = None
        self.cell_rects = []
        self.cell_states = []

        if self.file is None and self.size is not None:
            self.right_walls, self.bottom_walls = MazeGenerator().create_maze(self.size)
        else:
            loader = MazeLoader()
            self.size, self.right_walls, self.bottom_walls = loader.load(self.file)

        self.cell_flag        = 0
        self.start_end_states = [None, None]
        self.line_path        = []
        self._path_line_ids   = []   

    def render(self):
        for w in self.root.winfo_children():
            w.destroy()

        cell = max(min(500 // self.size, 500 // self.size), 4)
        cw = ch = self.size * cell

        container = ctk.CTkFrame(self.root, fg_color=BG)
        container.pack(expand=True, fill="both")

        canvas = ctk.CTkCanvas(container, width=cw, height=ch, bg=BG, highlightthickness=0)
        canvas.pack(expand=True)

        self.canvas = canvas
        self.cell   = cell

        self.cell_states = [[False] * self.size for _ in range(self.size)]
        self.cell_rects  = [[None]  * self.size for _ in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                x, y = col * cell, row * cell
                self.cell_rects[row][col] = canvas.create_rectangle(
                    x, y, x + cell, y + cell, fill=BG, outline=""
                )

        canvas.create_rectangle(0, 0, cw, ch, outline=WALL, width=2)

        for row in range(self.size):
            for col in range(self.size):
                x, y = col * cell, row * cell
                if self.right_walls[row][col] and col < self.size - 1:
                    canvas.create_line(x + cell, y, x + cell, y + cell, fill=WALL, width=2)
                if self.bottom_walls[row][col] and row < self.size - 1:
                    canvas.create_line(x, y + cell, x + cell, y + cell, fill=WALL, width=2)

        canvas.bind("<Button-1>", lambda e: self.on_cell_click(e.y // cell, e.x // cell))

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=8)

        ctk.CTkButton(btn_frame, text="← Back",
                      command=self.app.showMain).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Save",
                      command=lambda: self.saveMaze(self.right_walls, self.bottom_walls)).pack(side="left", padx=5)


    def _cell_center(self, col, row):
        """Возвращает экранные координаты центра ячейки (col, row)."""
        half = self.cell // 2
        return col * self.cell + half, row * self.cell + half

    def _draw_path_line(self):
        """Рисует маршрут одной ломаной линией через центры ячеек."""
        if len(self.line_path) < 2:
            return
        coords = []
        for x, y in self.line_path:
            cx, cy = self._cell_center(x, y)
            coords.extend([cx, cy])
        line_id = self.canvas.create_line(
            *coords,
            fill=CELL_PATH,
            width=2,                        
            capstyle="round",
            joinstyle="round",
        )
        self._path_line_ids.append(line_id)

    def _clear_path(self):
        """Удаляет нарисованную линию маршрута с холста."""
        for line_id in self._path_line_ids:
            self.canvas.delete(line_id)
        self._path_line_ids = []
        self.line_path = []




    def on_cell_click(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return

        if self.cell_flag == 2:
            self._clear_path()
            r0, c0 = self.start_end_states[0][1], self.start_end_states[0][0]
            r1, c1 = self.start_end_states[1][1], self.start_end_states[1][0]
            self.canvas.itemconfig(self.cell_rects[r0][c0], fill=BG)
            self.canvas.itemconfig(self.cell_rects[r1][c1], fill=BG)
            self.start_end_states = [None, None]
            self.cell_flag = 0

        elif self.cell_flag == 1:
            
            self.cell_flag = 2
            self.start_end_states[1] = (col, row)
            self.canvas.itemconfig(self.cell_rects[row][col], fill=CELL_END)

            pg = PathGenerator(self.start_end_states, self.right_walls, self.bottom_walls)
            self.line_path = pg.search_path() or []

            self._draw_path_line()

        else:

            self.cell_flag = 1
            self.start_end_states[0] = (col, row)
            self.canvas.itemconfig(self.cell_rects[row][col], fill=CELL_START)

        print(f"Нажата клетка: row={row}, col={col}, flag={self.cell_flag}")

    def saveMaze(self, right, bottom):
        MazeSave().save(len(right[0]), right, bottom)