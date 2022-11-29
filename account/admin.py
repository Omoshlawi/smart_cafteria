import typing
from typing import cast

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QLabel, \
    QVBoxLayout, QTreeWidget, QTreeWidgetItem, QDateTimeEdit, QMessageBox

from account.models import Account
from auth.models import User
from staff.states.base import BaseManager
from utils.utilities import template


class AccountAdmin(BaseManager):
    def __init__(self):
        super(AccountAdmin, self).__init__(QWidget(), template("accountManager.ui"))
        self._users = {user.user_id.value: user.username.value for user in User.all()}
        self.accountId = cast(QLineEdit, self.window.findChild(QLineEdit, 'accountId'))
        self.created = cast(QDateTimeEdit, self.window.findChild(QDateTimeEdit, 'created'))
        self.created.setDateTime(QDateTime.currentDateTime())
        self.users = cast(QComboBox, self.window.findChild(QComboBox, 'user'))
        self.balance = cast(QDoubleSpinBox, self.window.findChild(QDoubleSpinBox, 'balance'))
        self.addAccount = cast(QPushButton, self.window.findChild(QPushButton, 'addAccount'))
        self.updateAccount = cast(QPushButton, self.window.findChild(QPushButton, 'updateAccount'))
        self.deleteAccount = cast(QPushButton, self.window.findChild(QPushButton, 'deleteAccount'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self._current_account_id = -1
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.fillComboBox()
        self.addEventHandlers()
        self.setUpAccountsList()

    def cleaned_data(self) -> typing.Dict:
        self.error.clear()
        data = {'created': self.created.dateTime().toPyDateTime()}
        try:
            index = tuple(self._users.values()).index(self.users.currentText())
            data['user'] = tuple(self._users.keys())[index]
        except Exception as e:
            self.error.setText("Invalid User!!")
            return {}

        if not self.balance.value() or self.balance.value() < 0:
            self.error.setText("Invalid balance")
            return {}
        else:
            data['balance'] = self.balance.value()
        return data

    def addEventHandlers(self):
        self.addAccount.clicked.connect(self.handleAddAccount)
        self.updateAccount.clicked.connect(self.handleUpdateAccount)
        self.treeView.itemDoubleClicked.connect(self.onAccountDoubleClicked)
        self.deleteAccount.clicked.connect(self.handleDeleteAccount)
        # self.orderItems.clicked.connect(self.handleOrderItems)

    def handleDeleteAccount(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            account = Account.get(id=id_)
            dlg = QMessageBox(self.window)
            dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
            dlg.setWindowTitle("Warning!!")
            dlg.setText(
                f"Are you sure you want to delete Account-'{account.id.value}' for {User.get(user_id=account.user.value).get_full_name()}\n "
                f"This operation will permanently delete the record")
            status = dlg.exec()
            if status == QMessageBox.StandardButton.Apply:
                account.delete()
                self.setUpAccountsList()
                self.clearInputs()

    def onAccountDoubleClicked(self, item):
        id_ = int(item.text(0))
        self._current_account_id = id_
        account = Account.get(id=id_)
        self.populateFields(account.toJson())

    def populateFields(self, data):
        try:
            self.accountId.setText(str(data['id']))
            # todo fix the time populate bug
            self.created.setDateTime(QDateTime.fromString(data['created']))
            self.balance.setValue(data['balance'])
            self.users.setCurrentText(str(User.get(user_id=data['user'])))
        except Exception as e:
            # todo decide wether tho remove me or not
            print(e)

    def handleUpdateAccount(self):
        cd = self.cleaned_data()
        if cd and self._current_account_id != -1:
            account = Account.get(id=self._current_account_id)
            account.created.setValue(cd['created'])
            account.user.setValue(cd['user'])
            account.balance.setValue(cd['balance'])
            account.save()
            self.setUpAccountsList()
            self.clearInputs()

    def handleAddAccount(self):
        cd = self.cleaned_data()
        if cd:
            try:
                Account.create(
                    user=cd['user'],
                    created=cd['created'],
                    balance=cd['balance']
                )
                self.setUpAccountsList()
                self.clearInputs()
            except Exception as e:
                self.error.setText(str(e))

    def fillComboBox(self):
        self.users.addItems(self._users.values())
        self.users.setCurrentText('-------------------')

    def setUpAccountsList(self):
        self.treeView.clear()
        try:
            self.treeView.setColumnCount(4)
            self.treeView.setSortingEnabled(True)
            headers = [
                'id',
                'Created',
                'User',
                'Balance'
            ]
            self.treeView.setHeaderLabels(headers)
            for account in Account.all():
                values = [
                    str(account.id.value),
                    str(account.created.value),
                    str(User.get(user_id=account.user.value)),
                    str(account.balance.value)
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])

        except Exception as e:
            # todo display message box
            print(self.__module__, e)

    def clearInputs(self):
        self._current_account_id = -1
        self.users.setCurrentText("----------")
        self.created.setDateTime(QDateTime.currentDateTime())
        self.balance.setValue(0.0)
        self.accountId.clear()
