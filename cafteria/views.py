import os
from typing import cast

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget

# import
from settings import RESOURCES


class MainWindow:
    def __init__(self):
        self.window = QMainWindow()
        uic.loadUi(os.path.join(RESOURCES, 'layouts', "main.ui"), self.window)
        self.centralwidget = cast(QWidget, self.window.findChild(QWidget, 'centralwidget'))
        self.labelVsTecLogo = cast(QLabel, self.window.findChild(QLabel, 'vs_logo'))
        self.labelJkuatLogo = cast(QLabel, self.window.findChild(QLabel, 'jk_logo'))
        self.baseLayout = cast(QGridLayout, self.window.findChild(QGridLayout, 'baseLayout'))
        self.setUpUi()

    def setUpUi(self):
        self.window.setWindowTitle("Cafteria")
        self.centralwidget.setLayout(self.baseLayout)
        self.window.setWindowIcon(QIcon(os.path.join(RESOURCES, 'images', "vstec_yellow.png")))
        self.labelVsTecLogo.setPixmap(QPixmap(os.path.join(RESOURCES, 'images', "vstec_green.png")))
        self.labelJkuatLogo.setPixmap(QPixmap(os.path.join(RESOURCES, 'images', "jkuat-logo.webp")))
        self.labelJkuatLogo.setScaledContents(True)
        self.labelJkuatLogo.setMaximumSize(100, 100)
        self.labelVsTecLogo.setScaledContents(True)
        self.labelVsTecLogo.setMaximumSize(150, 150)
