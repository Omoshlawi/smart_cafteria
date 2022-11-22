from typing import cast

from PyQt6.QtWidgets import QWidget, QPushButton, QInputDialog
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
        self.addEventListerners()

    def addEventListerners(self):
        self.addStudent.clicked.connect(self.handleAddStudent)

    def handleAddStudent(self):
        studs = Student()
        fields = list(studs.get_filed_name())
        fields.remove(studs.getPk())

        print(fields)
        print("Adding")
