import typing
from datetime import datetime
from typing import cast

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QDateEdit, QGroupBox, QVBoxLayout, QGridLayout, QLCDNumber, \
    QMessageBox, QPushButton

from account.models import Account, Transactions
from components.menu_item import MenuItem
from food.models import Food
from orders.models import Orders, OrderItem
from settings import CASHIER_NUMBER
from students.models import Student
from utils.utilities import template, static
from view.generics import View


class StudentsView(View):
    def __init__(self, user):
        self.user = user
        self._menuItems: typing.List[MenuItem] = []
        self.student = self.getCurrentStudent(user)
        super(StudentsView, self).__init__(QMainWindow(), template('studentWindow.ui'))
        self.jkuat_logo = cast(QLabel, self.window.findChild(QLabel, 'jkuat_logo'))
        self.vstec_logo = cast(QLabel, self.window.findChild(QLabel, 'vstec_logo'))
        self.profileLayout = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'profileLayout'))
        self.groupBoxProfile = cast(QGroupBox, self.window.findChild(QGroupBox, 'groupBoxProfile'))
        self.foodMenu = cast(QGridLayout, self.window.findChild(QGridLayout, 'foodMenu'))
        self.time = cast(QLCDNumber, self.window.findChild(QLCDNumber, 'time'))
        self.orderNow = cast(QPushButton, self.window.findChild(QPushButton, 'orderNow'))
        self.groupBoxProfile.setLayout(self.profileLayout)
        self.vstec_logo.setPixmap(QPixmap(static("vstec_green.png")))
        self.jkuat_logo.setPixmap(QPixmap(static("jkuat-logo.webp")))
        self.jkuat_logo.setScaledContents(True)
        self.vstec_logo.setScaledContents(True)
        self.jkuat_logo.setMaximumSize(70, 70)
        self.vstec_logo.setMaximumSize(70, 70)
        self.cashierno = cast(QLineEdit, self.window.findChild(QLineEdit, 'cashierno'))
        self.accountBalance = cast(QLineEdit, self.window.findChild(QLineEdit, 'accountBalance'))
        self.cashierno.setText(str(CASHIER_NUMBER))
        self.date = cast(QDateEdit, self.window.findChild(QDateEdit, 'date'))
        self.date.setDate(datetime.now().date())
        self.regno = cast(QLineEdit, self.window.findChild(QLineEdit, 'regno'))
        self.email = cast(QLineEdit, self.window.findChild(QLineEdit, 'email'))
        self.name = cast(QLineEdit, self.window.findChild(QLineEdit, 'name'))
        self.mealtype = cast(QLabel, self.window.findChild(QLabel, 'mealtype'))
        self.totalCost = cast(QLineEdit, self.window.findChild(QLineEdit, 'totalCost'))
        self.initUiValues()
        self.setTimer()
        self.initFoodMenu()
        self.addEventHandler()
        self.window.showMaximized()

    def setTimer(self):
        timer = QtCore.QTimer(self.window)
        timer.timeout.connect(self.tickTime)
        timer.start(1)

    def tickTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.time.display(text)

    def initFoodMenu(self):
        self.foodMenu.addWidget(QLabel("Meal"), 0, 0)
        self.foodMenu.addWidget(QLabel("Price"), 0, 1)
        self.foodMenu.addWidget(QLabel("Quantity"), 0, 2)
        self.foodMenu.addWidget(QLabel("Total Cost"), 0, 3)
        self.addFoodToMenu()

    def addFoodToMenu(self):
        foods = Food.filter(available=True)
        row = 1
        for food in foods:
            menu_item = MenuItem(
                food,
                lambda: self.totalCost.setText(str(sum(float(item.totalCost.text()) for item in self._menuItems)))
            )
            self.foodMenu.addWidget(menu_item.meal, row, 0)
            self.foodMenu.addWidget(menu_item.price, row, 1)
            self.foodMenu.addWidget(menu_item.quantaSizer, row, 2)
            self.foodMenu.addWidget(menu_item.totalCost, row, 3)
            self._menuItems.append(menu_item)
            row += 1

    def addEventHandler(self):
        self.orderNow.clicked.connect(self.handleOrderAdd)

    def handleOrderAdd(self):
        balance = float(self.accountBalance.text())
        amount = float(self.totalCost.text().strip())
        if amount > balance:
            dialog = QMessageBox(self.window)
            dialog.setModal(True)
            dialog.setWindowTitle("Error!")
            dialog.setText(
                f"This operation Can't Proceed.You have insufficient balance of {self.accountBalance.text()}\n"
                f".Please Top up and try again")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            dialog.exec()
            return
        if amount > 0:
            dialog = QMessageBox(self.window)
            dialog.setModal(True)
            dialog.setWindowTitle("Confirmation")
            dialog.setText(
                f"\n{self.getFoodItems()}"
                f"\n\nKsh. {amount} will be deducted from you account"
                f"\nAre you sure you wanna proceed"
            )
            dialog.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
            status = dialog.exec()
            if status == QMessageBox.StandardButton.Yes:
                try:
                    # 1. create order
                    order = Orders.create(
                        user=self.user.user_id.value,
                        created=datetime.now(),
                    )
                    # 2. create order Items for the current order
                    for item in self._menuItems:
                        OrderItem.create(
                            order_id=order.id.value,
                            food=item.mealId,
                            quantity=int(item.quantaSizer.text),
                        )
                    transaction = Transactions.create(
                        order_transaction=order.id.value,
                        created=datetime.now(),
                    )
                    account = Account.get(user=self.user.user_id.value)
                    print(account.toJson())
                    account.debit(float(self.totalCost.text()))
                    print(account.toJson())
                    account.save()
                    self.initUiValues()
                except Exception as e:
                    print(e)

    def getFoodItems(self) -> str:
        # '{revenue:>7,} | {profit:>+6} | {percent:>7.2%}'
        return ("\n".join([f"{item.meal.text()} * {item.quantaSizer.text} = {item.totalCost.text()}"
                           f"" for item in self._menuItems if item.buyable]))

    def initUiValues(self):
        try:
            if self.student:
                self.regno.setText(self.student.registration_number.value)
                self.name.setText(self.user.get_full_name())
                self.email.setText(self.user.email.value)
                self.accountBalance.setText(str(Account.get(user=self.user.user_id.value).balance.value))
            hr = int(datetime.strftime(datetime.now(), "%H"))
            if hr in range(6, 8):
                self.mealtype.setText("BreakFirst")
            elif hr in range(11, 14):
                self.mealtype.setText("Lunch")
            elif hr in range(17, 20):
                self.mealtype.setText("Super")
            else:
                self.mealtype.clear()
        except Exception as e:
            # TODO DISPLAY RIGHT MESSAGE for errors such as object not found
            print(e)

    def getCurrentStudent(self, user):
        try:
            student = Student.get(user=user.user_id.value)
            return student
        except Exception as e:
            print(self.window)
            dlg = QMessageBox(self.window)
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setWindowTitle("Error!!")
            dlg.setText(str(e))
            status = dlg.exec()
