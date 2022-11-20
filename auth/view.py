import os
from typing import cast

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel

from settings import RESOURCES
from view.generics import View


class LoginView(View):
    def __init__(self):
        super().__init__(QDialog(), os.path.join(RESOURCES, 'layouts', "login.ui"))


