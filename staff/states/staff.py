from PyQt6.QtWidgets import QWidget
import os
from staff.states.base import BaseManager
from utils.utilities import template


class StaffManager(BaseManager):
    def __init__(self):
        super(StaffManager, self).__init__(QWidget(), template("staffManager.ui"))
