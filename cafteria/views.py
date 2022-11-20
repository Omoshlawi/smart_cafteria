import os
from typing import cast

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget

# import
from settings import RESOURCES
from view.generics import View


class MainWindow(View):
    def __init__(self):
        super().__init__(QMainWindow(), os.path.join(RESOURCES, 'layouts', "main.ui"))
        self.centralWidget = cast(QWidget, self.window.findChild(QWidget, 'centralwidget'))
        self.labelVsTecLogo = cast(QLabel, self.window.findChild(QLabel, 'vs_logo'))
        # self.labelJkuatLogo = cast(QLabel, self.window.findChild(QLabel, 'jk_logo'))
        self.setUpUi()

    def setUpUi(self):
        super(MainWindow, self).setUpUi()
        self.window.setWindowTitle("Cafteria")
        self.centralWidget.setLayout(self.baseLayout)
        self.labelVsTecLogo.setPixmap(QPixmap(os.path.join(RESOURCES, 'images', "vstec_green.png")))
        # self.labelJkuatLogo.setPixmap(QPixmap(os.path.join(RESOURCES, 'images', "jkuat-logo.webp")))
        # self.labelJkuatLogo.setScaledContents(True)
        # self.labelJkuatLogo.setMaximumSize(100, 100)
        self.labelVsTecLogo.setScaledContents(True)
        self.labelVsTecLogo.setMaximumSize(200, 200)
        self.window.setMinimumSize(1200, 800)

