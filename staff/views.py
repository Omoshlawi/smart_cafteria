from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget

from utils.utilities import template, static
from view.generics import View


class AdminView(View):
    def __init__(self, user):
        self.user = user
        super(AdminView, self).__init__(QMainWindow(), template("staffWindow.ui"))
        cast(QMainWindow, self.window).centralWidget().setLayout(self.baseLayout)
        self.currentAction = None
        self.currUser = cast(QLabel, self.window.findChild(QLabel, 'user'))
        self.jkuat_logo = cast(QLabel, self.window.findChild(QLabel, 'jkuat_logo'))
        self.vstec_logo = cast(QLabel, self.window.findChild(QLabel, 'vstec_logo'))
        self.vstec_logo.setPixmap(QPixmap(static("vstec_green.png")))
        self.jkuat_logo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuat_logo.setScaledContents(True)
        self.vstec_logo.setScaledContents(True)
        self.jkuat_logo.setMaximumSize(50, 50)
        self.vstec_logo.setMaximumSize(70, 70)
        self.initUiValue()
        self.addEventListener()
        self.window.show()

    def initUiValue(self):
        self.currUser.setText(f"{self.user.username.value}\nAdmin")

    def setCurrentAction(self, action: QWidget):
        self.currentAction = action

    def addEventListener(self):
        pass
