import os
import sys

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic


# import


class MainWindow:
    def __init__(self):
        app = QApplication(sys.argv)
        window: QMainWindow = uic.loadUi("./layouts/main.ui")
        window.setWindowTitle("Hellow")
        window.show()
        app.exec()
