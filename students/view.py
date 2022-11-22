from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel

from utils.utilities import template, static
from view.generics import View


class StudentsView(View):
    def __init__(self, user):
        super(StudentsView, self).__init__(QMainWindow(), template('studentWindow.ui'))
        cast(QMainWindow, self.window).centralWidget().setLayout(self.baseLayout)
        self.jkuat_logo = cast(QLabel, self.window.findChild(QLabel, 'jkuat_logo'))
        self.vstec_logo = cast(QLabel, self.window.findChild(QLabel, 'vstec_logo'))
        self.vstec_logo.setPixmap(QPixmap(static("vstec_green.png")))
        self.jkuat_logo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuat_logo.setScaledContents(True)
        self.vstec_logo.setScaledContents(True)
        self.jkuat_logo.setMaximumSize(70, 70)
        self.vstec_logo.setMaximumSize(70, 70)

        self.window.show()
