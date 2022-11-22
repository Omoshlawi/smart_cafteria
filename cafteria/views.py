from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget

from utils.utilities import template, static
# import
from view.generics import View


class MainWindow(View):
    def __init__(self):
        super().__init__(QMainWindow(), template("main.ui"))
        self.centralWidget = cast(QWidget, self.window.findChild(QWidget, 'centralwidget'))
        self.labelVsTecLogo = cast(QLabel, self.window.findChild(QLabel, 'vs_logo'))
        self.setUpUi()
        self.window.show()

    def setUpUi(self):
        self.window.setWindowTitle("Cafteria")
        self.centralWidget.setLayout(self.baseLayout)
        self.labelVsTecLogo.setPixmap(QPixmap(static("vstec_green.png")))
        self.labelVsTecLogo.setScaledContents(True)
        self.labelVsTecLogo.setMaximumSize(200, 200)
        self.window.setMinimumSize(1200, 800)


