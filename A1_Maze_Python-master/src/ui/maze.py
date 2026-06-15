import logging

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QFileDialog, QWidget

from modules.algorithm import bfs, get_path
from modules.exception import BaseMazeException
from modules.generation import MazeEller
from modules.load import Loader
from modules.maze import Cell, Maze

logging.basicConfig(
    filename='1.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)


class MazeWidget(QWidget):
    def __init__(
        self, main_window: QWidget | None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent, Qt.WindowType.Widget)
        self._clear_data()
        self.main_window: QWidget | None = main_window

    def _clear_data(self) -> None:
        self.maze: Maze | None = None
        self.STEP_X: int | None = None
        self.STEP_Y: int | None = None
        self.path: list[tuple[int, int]] | None = None
        self.exception: Exception | None = None
        self.start: tuple[int, int] | None = None
        self.end: tuple[int, int] | None = None

    def _download_button_pressed(self) -> None:
        file = QFileDialog.getOpenFileName(None, 'Open file')[0]
        logging.info(f'Download from file [{file}]')
        self._clear_data()
        try:
            self.maze = Loader().download(file)
            self.STEP_X = int(500 / self.maze.cols)
            self.STEP_Y = int(500 / self.maze.rows)
        except Exception as err:
            self.maze, self.STEP_X, self.STEP_Y = None, None, None
            self.exception = err
            logging.error(
                f'In _download_button_pressed() raised exception [{err.__class__.__name__}]',
                exc_info=err,
            )
        self.repaint()

    def _upload_button_pressed(self):
        dialog = QFileDialog(None)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            file = dialog.selectedFiles()[0]
            logging.info(f'Upload in file [{file}]')
            Loader().upload(file, self.maze)

    def _generate_button_pressed(self):
        self._clear_data()
        self.maze = MazeEller(
            int(self.main_window.ui.width.text()),
            int(self.main_window.ui.height.text()),
        )
        self.STEP_X = int(500 / self.maze.cols)
        self.STEP_Y = int(500 / self.maze.rows)
        self.maze.generate()
        self.repaint()

    def _find_path(self) -> None:
        try:
            if self.maze is None or self.STEP_X is None or self.STEP_Y is None:
                raise BaseMazeException('Maze is empty')
            logging.info(f'Find path from {self.start}, to {self.end}')
            frm: list[list[tuple[int, int]]] = bfs(self.maze, self.start)
            self.path = get_path(frm, self.end)
            logging.info(f'Path: {self.path}')
        except Exception as err:
            self.exception = err
            logging.error(f'In _find_path() raised exception [{err}]', exc_info=err)
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        qp: QPainter = QPainter()
        qp.begin(self)
        try:
            if self.maze and self.STEP_X and self.STEP_Y:
                self._draw_maze(qp)
                if self.path:
                    self._draw_path(qp)
                if self.start:
                    qp.setPen(QPen(Qt.green, 6, Qt.SolidLine))
                    qp.drawPoint(
                        self.start[0] * self.STEP_X + self.STEP_X // 2,
                        self.start[1] * self.STEP_Y + self.STEP_Y // 2,
                    )
        finally:
            qp.end()
        return super().paintEvent(event)

    def mousePressEvent(self, event) -> None:
        if self.maze and self.STEP_X and self.STEP_Y:
            pos: QPoint = event.pos()
            x: int = int(pos.x() // self.STEP_X)
            y: int = int(pos.y() // self.STEP_Y)
            if self.start is None:
                self.start = (x, y)
                self.repaint()
            elif self.end is None:
                self.end = (x, y)
                self._find_path()
            else:
                self.start, self.end, self.path = None, None, None
                self.repaint()

    def _draw_maze(self, qp) -> None:
        if self.maze is None:
            logging.info('Skip _draw_maze. Maze is empty')
            return

        logging.info('Start _draw_maze')
        pen: QPen = QPen(Qt.red, 2, Qt.SolidLine)

        qp.setPen(pen)
        for x in range(self.maze.cols):
            for y in range(self.maze.rows):
                cell: Cell = self.maze.field[y][x]
                if cell.walls['top']:
                    qp.drawLine(
                        x * self.STEP_X,
                        y * self.STEP_Y,
                        (x + 1) * self.STEP_X,
                        y * self.STEP_Y,
                    )
                if cell.walls['bottom']:
                    qp.drawLine(
                        x * self.STEP_X,
                        (y + 1) * self.STEP_Y,
                        (x + 1) * self.STEP_X,
                        (y + 1) * self.STEP_Y,
                    )
                if cell.walls['right']:
                    qp.drawLine(
                        (x + 1) * self.STEP_X,
                        y * self.STEP_Y,
                        (x + 1) * self.STEP_X,
                        (y + 1) * self.STEP_Y,
                    )
                if cell.walls['left']:
                    qp.drawLine(
                        x * self.STEP_X,
                        y * self.STEP_Y,
                        x * self.STEP_X,
                        (y + 1) * self.STEP_Y,
                    )

    def _draw_path(self, qp) -> None:
        if self.path is None:
            logging.info('Skip _draw_path. Path is empty')
            return

        logging.info('Start _draw_path')

        pen: QPen = QPen(Qt.green, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(len(self.path) - 1):
            qp.drawLine(
                self.path[i][0] * self.STEP_X + self.STEP_X / 2,
                self.path[i][1] * self.STEP_Y + self.STEP_Y / 2,
                self.path[i + 1][0] * self.STEP_X + self.STEP_X / 2,
                self.path[i + 1][1] * self.STEP_Y + self.STEP_Y / 2,
            )

    def _draw_exception(self, event, qp) -> None:
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, str(self.exception))
