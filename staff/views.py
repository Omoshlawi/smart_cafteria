from typing import cast

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QCommandLinkButton

from account.admin import AccountAdmin, TransactionAdmin
from orders.admin import OrderAdmin
from staff.states.base import BaseManager
from staff.states.food import FoodAdmin
from staff.states.staff import StaffManager
from staff.states.students import StudentManager
from utils.utilities import template, static
from view.generics import View


class AdminView(View):
    def __init__(self, user):
        self.user = user
        super(AdminView, self).__init__(QMainWindow(), template("staffWindow.ui"))
        self.currentState = None
        self.contentWidget = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'contentWidget'))
        self.manageStudents = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'manageStudents'))
        self.manageStaff = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'manageStaff'))
        self.manageSales = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'manageSales'))
        self.manageFood = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'manageFood'))
        self.dashBoard = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'dashBoard'))
        self.manageTransactions = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'transactions'))
        self.manageAccounts = cast(QCommandLinkButton, self.window.findChild(QCommandLinkButton, 'accounts'))
        self.currUser = cast(QLabel, self.window.findChild(QLabel, 'user'))
        self.jkuat_logo = cast(QLabel, self.window.findChild(QLabel, 'jkuat_logo'))
        self.vstec_logo = cast(QLabel, self.window.findChild(QLabel, 'vstec_logo'))
        self.vstec_logo.setPixmap(QPixmap(static("vstec_green.png")))
        self.jkuat_logo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuat_logo.setScaledContents(True)
        self.vstec_logo.setScaledContents(True)
        self.jkuat_logo.setMaximumSize(50, 50)
        self.vstec_logo.setMaximumSize(70, 70)
        self.initUiValue()
        self.window.showMaximized()

    def initUiValue(self):
        self.currUser.setText(f"{self.user.username.value}\nAdmin")
        self.setCurrentState(StudentManager())
        self.addEventListener()

    def setCurrentState(self, state: BaseManager):
        if self.currentState:
            self.contentWidget.removeWidget(self.currentState.window)
        self.currentState = state
        self.contentWidget.addWidget(state.window)

    def addEventListener(self):
        self.manageStudents.clicked.connect(lambda: self.setCurrentState(StudentManager()))
        self.manageStaff.clicked.connect(lambda: self.setCurrentState(StaffManager()))
        self.manageFood.clicked.connect(lambda: self.setCurrentState(FoodAdmin()))
        self.manageSales.clicked.connect(lambda: self.setCurrentState(OrderAdmin()))
        self.manageAccounts.clicked.connect(lambda: self.setCurrentState(AccountAdmin()))
        self.manageTransactions.clicked.connect(lambda: self.setCurrentState(TransactionAdmin()))
