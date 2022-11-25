from typing import cast

from PyQt6.QtWidgets import QWidget, QPushButton, QTreeWidget, QVBoxLayout, QTreeWidgetItem

from auth.models import User
from components.dialog import StudentRegistrationForm
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
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.setUpStudentsList()
        self.addEventListeners()

    def addEventListeners(self):
        self.addStudent.clicked.connect(self.handleAddStudent)

    def handleAddStudent(self):
        try:
            self.dialog = StudentRegistrationForm(self.window)
            status = self.dialog.exec()
            if status:
                self.setUpStudentsList()
        except Exception as e:
            print(e)

    def setUpStudentsList(self):
        students = Student.all()
        self.treeView.setColumnCount(5)
        self.treeView.setSortingEnabled(True)
        headers = [
            'Registration Number', 'First Name',
            'Last Name', 'Year of Study',
            'Email'
        ]
        self.treeView.setHeaderLabels(headers)
        for stud in students:
            # print(stud.get_class_attrs())
            user = User.get(user_id=stud.user.value)
            values = [
                stud.registration_number.value,
                user.first_name.value,
                user.last_name.value,
                str(stud.year_of_study.value),
                user.email.value
            ]
            self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
