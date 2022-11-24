from enum import Enum

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel

from db.models import Model
from utils.utilities import template
from view.generics import Dialog


class InputDialogBoxPurpose(Enum):
    CREATE = 0
    UPDATE = 1


class StudentRegistrationForm(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent, ui_file=template("studentsAddDialog.ui"))
        self.show()




