# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class Ui_View(object):
    def setupUi(self, View):
        if not View.objectName():
            View.setObjectName('View')
        View.resize(520, 620)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(View.sizePolicy().hasHeightForWidth())
        View.setSizePolicy(sizePolicy)
        View.setMinimumSize(QSize(520, 500))
        View.setMaximumSize(QSize(520, 700))
        View.setStyleSheet(
            'QWidget#View {\n'
            '	background-color: #222324;\n'
            '}\n'
            '\n'
            'QPushButton {\n'
            '	background-color: #222324;\n'
            '	color: #ffffff;\n'
            '}\n'
            '\n'
            'QLineEdit {\n'
            '	color: #ffffff;\n'
            '}\n'
            '\n'
            'QLabel {\n'
            '	color: #ffffff;\n'
            '}\n'
            '\n'
            'QFrame {\n'
            '	background-color: #222324;\n'
            '}\n'
            ''
        )
        self.verticalLayout_3 = QVBoxLayout(View)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.main_frame = QFrame(View)
        self.main_frame.setObjectName('main_frame')
        sizePolicy.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy)
        self.main_frame.setMinimumSize(QSize(500, 500))
        self.main_frame.setMaximumSize(QSize(500, 500))
        self.main_frame.setStyleSheet('')

        self.verticalLayout_3.addWidget(self.main_frame)

        self.frame_2 = QFrame(View)
        self.frame_2.setObjectName('frame_2')
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.splitter = QSplitter(self.frame_2)
        self.splitter.setObjectName('splitter')
        self.splitter.setOrientation(Qt.Horizontal)
        self.label_w = QLabel(self.splitter)
        self.label_w.setObjectName('label_w')
        sizePolicy.setHeightForWidth(self.label_w.sizePolicy().hasHeightForWidth())
        self.label_w.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.label_w)
        self.height = QLineEdit(self.splitter)
        self.height.setObjectName('height')
        self.splitter.addWidget(self.height)

        self.horizontalLayout_2.addWidget(self.splitter)

        self.splitter_2 = QSplitter(self.frame_2)
        self.splitter_2.setObjectName('splitter_2')
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.label_h = QLabel(self.splitter_2)
        self.label_h.setObjectName('label_h')
        sizePolicy.setHeightForWidth(self.label_h.sizePolicy().hasHeightForWidth())
        self.label_h.setSizePolicy(sizePolicy)
        self.splitter_2.addWidget(self.label_h)
        self.width = QLineEdit(self.splitter_2)
        self.width.setObjectName('width')
        self.splitter_2.addWidget(self.width)

        self.horizontalLayout_2.addWidget(self.splitter_2)

        self.generate_button = QPushButton(self.frame_2)
        self.generate_button.setObjectName('generate_button')
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.generate_button.sizePolicy().hasHeightForWidth()
        )
        self.generate_button.setSizePolicy(sizePolicy2)
        self.generate_button.setStyleSheet('')

        self.horizontalLayout_2.addWidget(self.generate_button)

        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame = QFrame(View)
        self.frame.setObjectName('frame')
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.download_button = QPushButton(self.frame)
        self.download_button.setObjectName('download_button')
        sizePolicy2.setHeightForWidth(
            self.download_button.sizePolicy().hasHeightForWidth()
        )
        self.download_button.setSizePolicy(sizePolicy2)
        self.download_button.setStyleSheet('')

        self.horizontalLayout.addWidget(self.download_button)

        self.upload_button = QPushButton(self.frame)
        self.upload_button.setObjectName('upload_button')
        sizePolicy2.setHeightForWidth(
            self.upload_button.sizePolicy().hasHeightForWidth()
        )
        self.upload_button.setSizePolicy(sizePolicy2)
        self.upload_button.setStyleSheet('')

        self.horizontalLayout.addWidget(self.upload_button)

        self.verticalLayout_3.addWidget(self.frame)

        self.retranslateUi(View)

        QMetaObject.connectSlotsByName(View)

    # setupUi

    def retranslateUi(self, View):
        View.setWindowTitle(QCoreApplication.translate('View', 'View', None))
        self.label_w.setText(QCoreApplication.translate('View', 'W', None))
        self.height.setText(QCoreApplication.translate('View', '5', None))
        self.label_h.setText(QCoreApplication.translate('View', 'H', None))
        self.width.setText(QCoreApplication.translate('View', '5', None))
        self.generate_button.setText(
            QCoreApplication.translate('View', 'Generate', None)
        )
        self.download_button.setText(
            QCoreApplication.translate('View', 'Downoad', None)
        )
        self.upload_button.setText(QCoreApplication.translate('View', 'Upload', None))

    # retranslateUi
