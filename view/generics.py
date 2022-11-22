import os
from typing import cast

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QMainWindow

from core.exceptions import TemplateDoesNotExistError
from utils.utilities import static


class View:
    def __init__(self, widget: QWidget, ui_file: str):
        if not os.path.exists(ui_file):
            raise TemplateDoesNotExistError(ui_file)
        self.window = widget
        uic.loadUi(ui_file, self.window)
        self.baseLayout = cast(QGridLayout, self.window.findChild(QGridLayout, 'baseLayout'))
        if isinstance(self.window, QMainWindow):
            if self.baseLayout:
                cast(QMainWindow, self.window).centralWidget().setLayout(self.baseLayout)
        else:
            if self.baseLayout:
                self.window.setLayout(self.baseLayout)
        self.window.setWindowIcon(QIcon(static("vstec_yellow.png")))

    # def getBaseLayout(self):
    #     raise NotImplementedError()
