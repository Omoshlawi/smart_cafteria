import typing
from typing import cast

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel

from auth.models import User
from utils.utilities import template
from view.generics import Form


class CredentialsForm(Form):
    def __init__(self, initial:dict, parent=None):
        super().__init__(parent=parent, ui_file=template("credentials.ui"))
        self.setWindowTitle("Reset Credentials")
        self.userName = cast(QLineEdit, self.findChild(QLineEdit, 'userName'))
        self.password = cast(QLineEdit, self.findChild(QLineEdit, 'password'))
        self.error = cast(QLabel, self.findChild(QLabel, 'error'))
        self.confirmPassword = cast(QLineEdit, self.findChild(QLineEdit, 'confirmPassword'))
        self.cancel = cast(QPushButton, self.findChild(QPushButton, 'cancel'))
        self.submit = cast(QPushButton, self.findChild(QPushButton, 'submit'))
        self._user_id = initial["user_id"]
        self.userName.setText(str(initial['username']))
        self.addEventListeners()

    def addEventListeners(self):
        self.cancel.clicked.connect(self.reject)
        self.submit.clicked.connect(self.onSubmit)

    def cleaned_data(self) -> typing.Dict:
        data = {}
        if not self.userName.text():
            self.error.setText("Please provide username")
            return {}
        else:
            data["userName"] = self.userName.text()
        if not self.password.text():
            self.error.setText("Please provide password")
            return {}
        else:
            data["password"] = self.password.text()

        if self.confirmPassword.text() != self.password.text():
            self.error.setText("Please confirm password")
            return {}
        return data

    def onSubmit(self):
        cd = self.cleaned_data()
        if cd:
            user = User.get(
                user_id=self._user_id,
            )
            user.username.setValue(cd['userName'])
            user.password.setValue(cd['password'])
            user.save()
            self.accept()
