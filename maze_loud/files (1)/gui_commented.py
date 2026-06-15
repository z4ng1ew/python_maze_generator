"""Графический интерфейс лабиринта на Tkinter.

Отвечает только за отрисовку и взаимодействие с пользователем.
Никакой бизнес-логики тут нет — она в src.maze.domain и других
доменных модулях. Это и есть принцип Чистой Архитектуры (Clean
Architecture): GUI зависит от домена, но домен не знает про GUI.
"""

import tkinter as tk
# tkinter — встроенный GUI-фреймворк Python.
# Это обёртка над Tcl/Tk (старая, но проверенная библиотека).

from tkinter import filedialog, messagebox
# filedialog — стандартные диалоги открытия/сохранения файла.
# messagebox — окошки с сообщениями (Информация, Ошибка, Вопрос).

from typing import Optional

from src.maze.domain import Maze
from src.maze.file_io import load_maze, MazeFileError


# Константы из задания
CANVAS_SIZE = 500          # размер поля 500x500 пикселей
WALL_THICKNESS = 2         # толщина стены 2 пикселя
BG_COLOR = "white"         # цвет фона
WALL_COLOR = "black"       # цвет стен


class MazeApp:
    """Главное приложение — окно с холстом и панелью инструментов.

    Класс держит ссылки на все виджеты (widget — элемент GUI) и
    на текущий лабиринт. Рисование делается в _render().
    """

    def __init__(self, root: tk.Tk) -> None:
        """Конструктор. root — главное окно Tk."""
        self.root = root
        self.root.title("A1_Maze_Py")
        # Optional[Maze] = либо Maze, либо None.
        # В Си было бы Maze* maze = NULL;
        self.maze: Optional[Maze] = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Собирает виджеты в окно. Подчёркивание = приватный метод."""

        # Верхняя панель с кнопками
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # pack — это менеджер компоновки.
        # side=tk.TOP — приклеить к верху.
        # fill=tk.X — растянуть по горизонтали.

        tk.Button(toolbar, text="Открыть", command=self._on_open).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        # command=self._on_open — обработчик нажатия.
        # В Си это callback-функция (указатель на функцию).

        # Заглушки для будущих частей задания. state=tk.DISABLED — кнопка
        # серая, нажать нельзя. Включим в следующих частях.
        tk.Button(toolbar, text="Генерировать", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Решить", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        tk.Button(toolbar, text="Пещера", state=tk.DISABLED).pack(
            side=tk.LEFT, padx=2, pady=2
        )

        # Холст для рисования
        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg=BG_COLOR,
            highlightthickness=0,  # убрать рамку фокуса по умолчанию
        )
        self.canvas.pack(padx=10, pady=10)

        # Статусная строка внизу
        self.status_var = tk.StringVar(value="Откройте файл лабиринта")
        # StringVar — это «реактивная» строковая переменная Tk.
        # Когда меняешь её через .set(), Label автоматически
        # перерисовывается. Аналог: observer-паттерн.
        tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor=tk.W,  # выровнять текст по левому краю (West)
            bd=1,
            relief=tk.SUNKEN,
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def _on_open(self) -> None:
        """Обработчик кнопки 'Открыть'."""
        path = filedialog.askopenfilename(
            title="Выберите файл лабиринта",
            filetypes=[("Файл лабиринта", "*.txt"), ("Все файлы", "*.*")],
        )
        # askopenfilename вернёт пустую строку, если пользователь
        # нажал Cancel. Тогда выходим без действий.
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
        """Рисует текущий лабиринт на холсте.

        Алгоритм:
          1. Стираем всё со старого кадра.
          2. Считаем размер ячейки в пикселях, чтобы лабиринт занял весь
             холст 500x500.
          3. Рисуем внешнюю рамку (это правый и нижний внешние края +
             левый и верхний — отдельно).
          4. Внутренние вертикальные стены: для каждой ячейки (r, c),
             где c < cols-1 и vertical_walls[r][c] == 1.
          5. Внутренние горизонтальные стены: симметрично.
        """
        self.canvas.delete("all")  # очистить холст

        if self.maze is None:
            return

        m = self.maze
        # Делим холст на rows строк и cols столбцов.
        # Используем float для аккуратной отрисовки, без накопления
        # ошибки округления.
        cell_w = CANVAS_SIZE / m.cols
        cell_h = CANVAS_SIZE / m.rows

        # === Внешняя рамка ===
        # Левая и верхняя — рисуем сами (их в матрицах нет).
        # Правая и нижняя — берутся из последнего столбца/строки матриц,
        # они всегда == 1.
        self.canvas.create_rectangle(
            0, 0, CANVAS_SIZE, CANVAS_SIZE,
            width=WALL_THICKNESS, outline=WALL_COLOR,
        )

        # === Внутренние вертикальные стены ===
        # vertical_walls[r][c] == 1 → стена справа от ячейки (r, c).
        # Координата X стены = (c + 1) * cell_w
        # Стена идёт по Y от r*cell_h до (r+1)*cell_h.
        # Внешний правый край (c == cols - 1) уже нарисован рамкой.
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

        # === Внутренние горизонтальные стены ===
        # horizontal_walls[r][c] == 1 → стена снизу от ячейки (r, c).
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
    """Создаёт окно и запускает событийный цикл.

    mainloop() — это бесконечный цикл, который слушает
    события окна (клик, ввод, закрытие). Возвращается, только
    когда пользователь закроет окно. Аналог: GetMessage/DispatchMessage
    в Win32.
    """
    root = tk.Tk()
    MazeApp(root)
    root.mainloop()
