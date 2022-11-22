from typing import cast

from PyQt6.QtWidgets import QWidget, QPushButton

from components.dialog import InputDialogBox, InputDialogBoxPurpose
from students.models import Student
from utils.utilities import template
from .base import BaseManager


class StudentManager(BaseManager):
    def __init__(self):
        super(StudentManager, self).__init__(QWidget(), template("studentsManager.ui"))
        self.addStudent = cast(QPushButton, self.window.findChild(QPushButton, 'addStudent'))
        self.deleteStudent = cast(QPushButton, self.window.findChild(QPushButton, 'deleteStudent'))
        self.resetPassword = cast(QPushButton, self.window.findChild(QPushButton, 'resetPassword'))
        self.updateStudent = cast(QPushButton, self.window.findChild(QPushButton, 'updateStudent'))
        self.addEventListeners()

    def addEventListeners(self):
        self.addStudent.clicked.connect(self.handleAddStudent)

    def handleAddStudent(self):
        dialog = InputDialogBox(parent=self.window, instance=Student(), purpose=InputDialogBoxPurpose.CREATE)
        print(dialog.exec())

