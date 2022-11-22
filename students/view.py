from datetime import datetime
from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QDateEdit

from settings import CASHIER_NUMBER
from students.models import Student
from utils.utilities import template, static
from view.generics import View


class StudentsView(View):
    def __init__(self, user):
        self.user = user
        self.student = self.getCurrentStudent(user)
        super(StudentsView, self).__init__(QMainWindow(), template('studentWindow.ui'))
        cast(QMainWindow, self.window).centralWidget().setLayout(self.baseLayout)
        self.jkuat_logo = cast(QLabel, self.window.findChild(QLabel, 'jkuat_logo'))
        self.vstec_logo = cast(QLabel, self.window.findChild(QLabel, 'vstec_logo'))
        self.vstec_logo.setPixmap(QPixmap(static("vstec_green.png")))
        self.jkuat_logo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuat_logo.setScaledContents(True)
        self.vstec_logo.setScaledContents(True)
        self.jkuat_logo.setMaximumSize(70, 70)
        self.vstec_logo.setMaximumSize(70, 70)
        self.cashierno = cast(QLineEdit, self.window.findChild(QLineEdit, 'cashierno'))
        self.cashierno.setText(str(CASHIER_NUMBER))
        self.date = cast(QDateEdit, self.window.findChild(QDateEdit, 'date'))
        self.date.setDate(datetime.now().date())
        self.regno = cast(QLineEdit, self.window.findChild(QLineEdit, 'regno'))
        self.name = cast(QLineEdit, self.window.findChild(QLineEdit, 'name'))
        self.mealtype = cast(QLabel, self.window.findChild(QLabel, 'mealtype'))
        self.initUiValues()
        self.window.show()

    def initUiValues(self):
        if self.student:
            self.regno.setText(self.student.registration_number.value)
            self.name.setText(self.user.get_full_name())
        hr = int(datetime.strftime(datetime.now(), "%H"))
        if hr in range(6, 8):
            self.mealtype.setText("BreakFirst")
        elif hr in range(11, 14):
            self.mealtype.setText("Lunch")
        elif hr in range(17, 20):
            self.mealtype.setText("Super")
        else:
            self.mealtype.setText("")

    def getCurrentStudent(self, user):
        try:
            student = Student.get(user=user.user_id.value)
            return student
        except Exception as e:
            # TODO ADD ERROR MESSAFE
            print(f"{e=}")
