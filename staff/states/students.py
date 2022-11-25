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
        self.updateStudent.clicked.connect(self.handleUpdateStudent)

    def handleAddStudent(self):
        try:
            self.dialog = StudentRegistrationForm(self.window)
            status = self.dialog.exec()
            if status:
                self.setUpStudentsList()
        except Exception as e:
            print(e)

    def handleUpdateStudent(self):
        curr_item = self.treeView.currentItem()
        # print(self.treeView.currentIndex().row())
        # print(self.treeView.currentIndex().column())
        if curr_item:
            data = {}
            id_ = int(curr_item.text(0))
            user = User.get(user_id=id_)
            stud = Student.get(user=id_)
            data.update(user.toJson())
            data.update(stud.toJson())
            self.updateDialog = StudentRegistrationForm(self.window, data)
            status = self.updateDialog.exec()
            if status:
                self.setUpStudentsList()

    def setUpStudentsList(self):
        self.treeView.clear()
        students = Student.all()
        self.treeView.setColumnCount(5)
        self.treeView.setSortingEnabled(True)
        headers = [
            'id',
            'Registration Number',
            'First Name',
            'Last Name',
            'Year of Study',
            'Email',
            'Course'
        ]
        self.treeView.setHeaderLabels(headers)
        for stud in students:
            user = User.get(user_id=stud.user.value)
            values = [
                str(user.user_id.value),
                stud.registration_number.value,
                user.first_name.value,
                user.last_name.value,
                str(stud.year_of_study.value),
                user.email.value,
                stud.course.value
            ]
            self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
