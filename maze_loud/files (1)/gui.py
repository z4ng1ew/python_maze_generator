"""Графический интерфейс лабиринта на Tkinter."""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

from src.maze.domain import Maze
from src.maze.file_io import load_maze, MazeFileError


CANVAS_SIZE = 500
WALL_THICKNESS = 2
BG_COLOR = "white"
WALL_COLOR = "black"


class MazeApp:
    """Главное приложение."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("A1_Maze_Py")
        self.maze: Optional[Maze] = None
        self._build_ui()

    def _build_ui(self) -> None:
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Открыть", command=self._on_open).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Генерировать", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Решить", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Пещера", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )

        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        self.status_var = tk.StringVar(value="Откройте файл лабиринта")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor=tk.W,
            bd=1,
            relief=tk.SUNKEN,
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def _on_open(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите файл лабиринта",
            filetypes=[("Файл лабиринта", "*.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return

        try:
            self.maze = load_maze(path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден")
            return
        except MazeFileError as exc:
            messagebox.showerror("Неверный формат файла", str(exc))
            return

        self._render()
        self.status_var.set(
            f"Загружен лабиринт {self.maze.rows}x{self.maze.cols}: {path}"
        )

    def _render(self) -> None:
        self.canvas.delete("all")

        if self.maze is None:
            return

        m = self.maze
        cell_w = CANVAS_SIZE / m.cols
        cell_h = CANVAS_SIZE / m.rows

        self.canvas.create_rectangle(
            0, 0, CANVAS_SIZE, CANVAS_SIZE,
            width=WALL_THICKNESS, outline=WALL_COLOR,
        )

        for r in range(m.rows):
            for c in range(m.cols - 1):
                if m.vertical_walls[r][c] == 1:
                    x = (c + 1) * cell_w
                    y1 = r * cell_h
                    y2 = (r + 1) * cell_h
                    self.canvas.create_line(
                        x, y1, x, y2,
                        width=WALL_THICKNESS, fill=WALL_COLOR,
                    )

        for r in range(m.rows - 1):
            for c in range(m.cols):
                if m.horizontal_walls[r][c] == 1:
                    y = (r + 1) * cell_h
                    x1 = c * cell_w
                    x2 = (c + 1) * cell_w
                    self.canvas.create_line(
                        x1, y, x2, y,
                        width=WALL_THICKNESS, fill=WALL_COLOR,
                    )


def run_app() -> None:
    root = tk.Tk()
    MazeApp(root)
    root.mainloop()
