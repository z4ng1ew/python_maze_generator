# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtCore import QRect
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui.form_ui import Ui_View
from ui.maze import MazeWidget


class View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_View()
        self.ui.setupUi(self)

        self.ui.int_validator = QIntValidator(1, 50)
        self.ui.width.setValidator(self.ui.int_validator)
        self.ui.height.setValidator(self.ui.int_validator)
        self.maze_widget = MazeWidget(self, self.ui.main_frame)
        self.maze_widget.setObjectName('maze_widget')
        self.maze_widget.setGeometry(QRect(0, 0, 500, 500))
        self.ui.download_button.clicked.connect(
            self.maze_widget._download_button_pressed
        )
        self.ui.upload_button.clicked.connect(self.maze_widget._upload_button_pressed)
        self.ui.generate_button.clicked.connect(
            self.maze_widget._generate_button_pressed
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = View()
    widget.show()
    sys.exit(app.exec())
