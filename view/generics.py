import os

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout
from typing import cast
from core.exceptions import TemplateDoesNotExistError
from settings import RESOURCES


class View:
    def __init__(self, widget: QWidget, ui_file: str):
        if not os.path.exists(ui_file):
            raise TemplateDoesNotExistError(ui_file)
        self.window = widget
        uic.loadUi(ui_file, self.window)
        self.baseLayout = cast(QGridLayout, self.window.findChild(QGridLayout, 'baseLayout'))

    def setUpUi(self):
        self.window.setWindowIcon(QIcon(os.path.join(RESOURCES, 'images', "vstec_yellow.png")))
