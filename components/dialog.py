import typing
from enum import Enum
from typing import cast

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel

from auth.models import User
from students.models import Student
from utils.utilities import template
from view.generics import Dialog


class InputDialogBoxPurpose(Enum):
    CREATE = 0
    UPDATE = 1


class StudentRegistrationForm(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent, ui_file=template("studentsAddDialog.ui"))
        self.firstName = cast(QLineEdit, self.findChild(QLineEdit, 'firstName'))
        self.lastName = cast(QLineEdit, self.findChild(QLineEdit, 'lastName'))
        self.email = cast(QLineEdit, self.findChild(QLineEdit, 'email'))
        self.regNo = cast(QLineEdit, self.findChild(QLineEdit, 'regNo'))
        self.yos = cast(QLineEdit, self.findChild(QLineEdit, 'yos'))
        self.course = cast(QLineEdit, self.findChild(QLineEdit, 'course'))
        self.cancel = cast(QPushButton, self.findChild(QPushButton, 'cancel'))
        self.submit = cast(QPushButton, self.findChild(QPushButton, 'submit'))
        self.error = cast(QLabel, self.findChild(QLabel, 'error'))
        self.setModal(True)
        self.addEventListeners()

    def addEventListeners(self):
        self.cancel.clicked.connect(self.reject)
        self.submit.clicked.connect(self.onSubmit)

    def cleaned_data(self) -> typing.Dict:
        data = {}
        if not self.firstName.text():
            self.error.setText("Please Enter first name")
            return {}
        else:
            data['firstName'] = self.firstName.text()
        if not self.lastName.text():
            self.error.setText("Please enter students last name")
            return {}
        else:
            data['lastName'] = self.lastName.text()
        if not self.email.text():
            self.error.setText("Please enter students email")
            return {}
        else:
            data['email'] = self.email.text()
        if not self.regNo.text():
            self.error.setText("Please enter students registration Number")
            return {}
        else:
            data['regNo'] = self.regNo.text()
        try:
            d = int(self.yos.text())
            data['yos'] = d
        except ValueError:
            self.error.setText("Please enter valid year of study")
            return {}
        if not self.course.text():
            self.error.setText("Please enter students course")
            return {}
        else:
            data['course'] = self.course.text()
        return data

    def onSubmit(self):
        cd = self.cleaned_data()
        if cd:
            try:
                user = User.create(
                    username=cd['regNo'],
                    email=cd['email'],
                    first_name=cd['firstName'],
                    last_name=cd['lastName'],
                    password=cd['regNo']
                )
                stud = Student.create(
                    user=user.user_id.value,
                    registration_number=cd['regNo'],
                    year_of_study=cd['yos'],
                    course=cd['course']
                )
                self.accept()
            except Exception as e:
                self.error.setText(str(e))
