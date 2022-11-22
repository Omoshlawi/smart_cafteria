import os
from typing import cast

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout

from core.exceptions import TemplateDoesNotExistError
from utils.utilities import static


class View:
    def __init__(self, widget: QWidget, ui_file: str):
        if not os.path.exists(ui_file):
            raise TemplateDoesNotExistError(ui_file)
        self.window = widget
        uic.loadUi(ui_file, self.window)
        self.baseLayout = cast(QGridLayout, self.window.findChild(QGridLayout, 'baseLayout'))
        self.window.setWindowIcon(QIcon(static("vstec_yellow.png")))
        self.window.setLayout(self.baseLayout)



