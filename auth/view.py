from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QPushButton

from auth.models import User
from core.exceptions import ObjectDoesNotExistError, MultipleObjectsError
from settings import CASHIER_NUMBER
from staff.views import AdminView
from students.view import StudentsView
from utils.utilities import static
from utils.utilities import template
from view.generics import View


class LoginView(View):
    def __init__(self):
        super().__init__(QDialog(), template("login.ui"))
        self.next = None
        self.cashier_no = cast(QLineEdit, self.window.findChild(QLineEdit, 'cashier_no'))
        self.cashier_no.setText(str(CASHIER_NUMBER))
        self.jkuatLogo = cast(QLabel, self.window.findChild(QLabel, 'jkuatLogo'))
        self.jkuatLogo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuatLogo.setScaledContents(True)
        self.jkuatLogo.setMaximumSize(70, 70)
        self.signInBtn = cast(QPushButton, self.window.findChild(QPushButton, 'loginBtn'))
        self.password = cast(QLineEdit, self.window.findChild(QLineEdit, 'passwordInput'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self.success = cast(QLabel, self.window.findChild(QLabel, 'success'))
        self.userName = cast(QLineEdit, self.window.findChild(QLineEdit, 'usernameInput'))
        self.toggleShowPassword = cast(QCheckBox, self.window.findChild(QCheckBox, 'toggleShowPassword'))
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.addEventHandlers()

    def addEventHandlers(self):
        self.toggleShowPassword.toggled.connect(self.handleToggle)
        self.signInBtn.clicked.connect(self.handleLogin)

    def handleToggle(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def handleLogin(self):
        try:
            user = User.get(username=self.userName.text(), password=self.password.text())
            self.error.setText("")
            self.success.setText("Login success!")
            if user.is_admin.value:
                self.next = AdminView(user)
            else:
                self.next = StudentsView(user)
            self.window.close()
        except ObjectDoesNotExistError:
            self.error.setText("Invalid username or password")
        except MultipleObjectsError:
            self.error.setText("Invalid username or password")
        except Exception as e:
            print(f'{e=}')
