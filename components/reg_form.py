import typing
from typing import cast

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QComboBox

from auth.models import User
from students.models import Student
from utils.utilities import template
from view.generics import Dialog


class StudentRegistrationForm(Dialog):
    def __init__(self, parent=None, initial: dict = None):
        super().__init__(parent=parent, ui_file=template("studentsAddDialog.ui"))
        self._update = False
        if initial:
            self._update = True
            self._student_id = initial['id']
            self._users = {user.user_id.value: user.username.value for user in User.all()}
        self.firstName = cast(QLineEdit, self.findChild(QLineEdit, 'firstName'))
        self.lastName = cast(QLineEdit, self.findChild(QLineEdit, 'lastName'))
        self.email = cast(QLineEdit, self.findChild(QLineEdit, 'email'))
        self.regNo = cast(QLineEdit, self.findChild(QLineEdit, 'regNo'))
        self.yos = cast(QLineEdit, self.findChild(QLineEdit, 'yos'))
        self.course = cast(QLineEdit, self.findChild(QLineEdit, 'course'))
        self.cancel = cast(QPushButton, self.findChild(QPushButton, 'cancel'))
        self.submit = cast(QPushButton, self.findChild(QPushButton, 'submit'))
        self.error = cast(QLabel, self.findChild(QLabel, 'error'))
        self.comboUser = cast(QComboBox, self.findChild(QComboBox, 'comboUser'))
        if self._update:
            self.fillComboBox()
            self.populate(data=initial)
        else:
            self.baseLayout.removeRow(0)

        self.setModal(True)
        self.addEventListeners()

    def fillComboBox(self):
        # if self._update:
        self.comboUser.addItems(self._users.values())
        self.comboUser.setCurrentIndex(0)

    def populate(self, data: dict):
        try:
            self.comboUser.setCurrentText(data["username"])
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
        if self._update:
            try:
                index = tuple(self._users.values()).index(self.comboUser.currentText())
                data['user'] = tuple(self._users.keys())[index]
            except Exception as e:
                self.error.setText("Invalid User!!")
                return {}

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
                    stud = Student.get(
                        id=self._student_id
                    )
                    stud.user.setValue(cd['user'])
                    stud.registration_number.setValue(cd['regNo']),
                    stud.year_of_study.setValue(cd['yos']),
                    stud.course.setValue(cd['course'])
                    stud.save()
                    user = User(
                        user_id=stud.user.value,
                        username=cd['regNo'],
                        email=cd['email'],
                        first_name=cd['firstName'],
                        last_name=cd['lastName'],
                        password=cd['regNo']
                    )
                    user.save()

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
