from PyQt6.QtWidgets import QMainWindow

from utils.utilities import template
from view.generics import View


class AdminView(View):
    def __init__(self, user):
        super(AdminView, self).__init__(QMainWindow(), template("staffWindow.ui"))
