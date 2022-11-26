import typing
from typing import cast

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel

from auth.models import User
from students.models import Student
from utils.utilities import template
from view.generics import Dialog


class StudentRegistrationForm(Dialog):
    def __init__(self, parent=None, initial: dict = None):
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
        self._update = False
        if initial:
            self._update = True
            self._user_id = initial['user_id']
            self.populate(data=initial)

        self.setModal(True)
        self.addEventListeners()

    def populate(self, data: dict):
        try:
            self.firstName.setText(data['first_name'])
            self.lastName.setText(data['last_name'])
            self.email.setText(data['email'])
            self.course.setText(data['course'])
            self.regNo.setText(data['registration_number'])
            self.yos.setText(str(data['year_of_study']))
        except Exception as e:
            # TODO handle data appropriately
            print(e)

    def addEventListeners(self):
        self.cancel.clicked.connect(self.reject)
        self.submit.clicked.connect(self.onSubmit)

    def cleaned_data(self) -> typing.Dict:
        data = {}
        if not self.firstName.text():
            self.error.setText("Please Enter first name")
            self.firstName.setFocus()
            return {}
        else:
            data['firstName'] = self.firstName.text()
        if not self.lastName.text():
            self.error.setText("Please enter students last name")
            self.lastName.setFocus()
            return {}
        else:
            data['lastName'] = self.lastName.text()
        if not self.email.text():
            self.error.setText("Please enter students email")
            self.email.setFocus()
            return {}
        else:
            data['email'] = self.email.text()
        if not self.regNo.text():
            self.error.setText("Please enter students registration Number")
            self.regNo.setFocus()
            return {}
        else:
            data['regNo'] = self.regNo.text()
        try:
            d = int(self.yos.text())
            data['yos'] = d
        except ValueError:
            self.error.setText("Please enter valid year of study")
            self.yos.setFocus()
            return {}
        if not self.course.text():
            self.error.setText("Please enter students course")
            self.course.setFocus()
            return {}
        else:
            data['course'] = self.course.text()
        return data

    def onSubmit(self):
        cd = self.cleaned_data()
        if cd:
            try:
                if self._update:
                    user = User(
                        user_id=self._user_id,
                        username=cd['regNo'],
                        email=cd['email'],
                        first_name=cd['firstName'],
                        last_name=cd['lastName'],
                        password=cd['regNo']
                    )
                    user.save()
                    stud = Student(
                        user=user.user_id.value,
                        registration_number=cd['regNo'],
                        year_of_study=cd['yos'],
                        course=cd['course']
                    )
                    stud.save()
                else:
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
