import typing
from typing import cast

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QLabel, \
    QVBoxLayout, QTreeWidget, QTreeWidgetItem, QDateTimeEdit, QMessageBox, QCheckBox

from account.models import Account, Transactions
from auth.models import User
from core.exceptions import ObjectDoesNotExistError
from orders.models import Orders
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


class TransactionAdmin(BaseManager):
    def __init__(self):
        super(TransactionAdmin, self).__init__(QWidget(), template("transactionManager.ui"))
        self._orders = {order.id.value: f"ord-{order.id.value}" for order in Orders.all()}
        self.transactionId = cast(QLineEdit, self.window.findChild(QLineEdit, 'transactionId'))
        self.created = cast(QDateTimeEdit, self.window.findChild(QDateTimeEdit, 'created'))
        self.created.setDateTime(QDateTime.currentDateTime())
        self.orders = cast(QComboBox, self.window.findChild(QComboBox, 'orders'))
        self.addTransaction = cast(QPushButton, self.window.findChild(QPushButton, 'addTransaction'))
        self.updateTransaction = cast(QPushButton, self.window.findChild(QPushButton, 'updateTransaction'))
        self.deleteTransaction = cast(QPushButton, self.window.findChild(QPushButton, 'deleteTransaction'))
        self.rollBackOnDelete = cast(QCheckBox, self.window.findChild(QCheckBox, 'rollBackOnDelete'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self._current_transaction_id = -1
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.fillComboBox()
        self.addEventHandlers()
        self.setUpTransactionsList()

    def fillComboBox(self):
        self.orders.addItems(self._orders.values())
        self.orders.setCurrentText('-------------------')

    def addEventHandlers(self):
        self.addTransaction.clicked.connect(self.handleAddTrans)
        self.updateTransaction.clicked.connect(self.handleUpdateTrans)
        self.treeView.itemDoubleClicked.connect(self.onTransItemDoubleClicked)
        self.deleteTransaction.clicked.connect(self.handleDeleteTrans)

    def onTransItemDoubleClicked(self, item):
        id_ = int(item.text(0))
        self._current_transaction_id = id_
        transaction = Transactions.get(id=id_)
        self.populateFields(transaction.toJson())

    def populateFields(self, data):
        try:
            self.transactionId.setText(str(data['id']))
            # todo fix the time populate bug
            self.created.setDateTime(QDateTime.fromString(data['created']))
            self.orders.setCurrentText(f"ord-{data['order_transaction']}")
        except Exception as e:
            # todo decide wether tho remove me or not
            print(e)

    def handleAddTrans(self):
        cd = self.cleaned_data()
        if cd:
            order = Orders.get(id=cd['order_transaction'])
            try:
                account = Account.get(user=order.user.value)
                bal = account.balance.value
                if order.getTotalCost() > bal:
                    self.error.setText("Insufficient account balance")
                    return
                account.balance.setValue(bal - order.getTotalCost())
                order.paid.setValue(True)
                order.save()
                account.save()
                Transactions.create(
                    order_transaction=cd['order_transaction'],
                    created=cd['created']
                )
                self.setUpTransactionsList()
                self.clearInputs()
            except ObjectDoesNotExistError:
                self.error.setText(
                    f"Order User '{User.get(user_id=order.user.value).username.value}' has no account, Please create one")
            except Exception as e:
                self.error.setText(str(e))

    def handleDeleteTrans(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            try:
                id_ = int(curr_item.text(0))
                transaction = Transactions.get(id=id_)
                order = Orders.get(id=transaction.order_transaction.value)
                account = Account.get(user=order.user.value)
                dlg = QMessageBox(self.window)
                dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
                dlg.setWindowTitle("Warning!!")
                dlg.setText(
                    f"Are you sure you want to delete Transaction-'{transaction.id.value}' for {User.get(user_id=order.user.value).get_full_name()}\n "
                    f"This operation will permanently delete the record {'and rollback payment' if self.rollBackOnDelete.isChecked() else ''}")
                status = dlg.exec()
                if status == QMessageBox.StandardButton.Apply:
                    if self.rollBackOnDelete.isChecked():
                        bal = account.balance.value
                        account.balance.setValue(bal + order.getTotalCost())
                        order.paid.setValue(False)
                        account.save()
                        order.save()
                    transaction.delete()
                    self.setUpTransactionsList()
                    self.clearInputs()
            except Exception as e:
                self.error.setText(str(e))

    def handleUpdateTrans(self):
        cd = self.cleaned_data()
        if cd and self._current_transaction_id != -1:
            transaction = Transactions.get(id=self._current_transaction_id)
            order_dict = Orders.get(id=transaction.order_transaction.value).toJson()
            order2_dict = Orders.get(id=cd['order_transaction']).toJson()
            try:
                account_dict = Account.get(user=order_dict['user']).toJson()
                account2_dict = Account.get(user=order2_dict['user']).toJson()
                bal = account_dict['balance']
                bal2 = account2_dict['balance']
                if transaction.order_transaction.value != cd[
                    'order_transaction'] and order2_dict['totalCost'] <= account2_dict['balance']:
                    # rollback the previous one and subtract the current
                    # 1. rollback trans of previous order
                    account = Account.get(id=account_dict['id'])
                    account.balance.setValue(float(bal + order_dict['totalCost']))
                    order = Orders.get(id=order_dict['id'])
                    order.paid.setValue(False)
                    account.save()
                    order.save()
                    # 2. Trasact account of new order
                    account2 = Account.get(id=account_dict['id'])
                    account2.balance.setValue(bal2 - order2_dict['totalCost'])
                    order2 = Orders.get(id=order2_dict['id'])
                    order2.paid.setValue(True)
                    order2.save()
                    account2.save()
                    transaction.order_transaction.setValue(cd['order_transaction'])
                transaction.created.setValue(cd['created'])
                transaction.save()
                self.setUpTransactionsList()
                self.clearInputs()
            except ObjectDoesNotExistError as e:
                self.error.setText(
                    f"Order User '{User.get(user_id=order.user.value).username.value}' or {User.get(user_id=order2.user.value).username.value} has no account, Please create one")
            except Exception as e:
                self.error.setText(str(e))

    def setUpTransactionsList(self):
        self.treeView.clear()
        try:
            self.treeView.setColumnCount(5)
            self.treeView.setSortingEnabled(True)
            headers = [
                'id',
                'User',
                'Created',
                'Order',
                'Amount'
            ]
            self.treeView.setHeaderLabels(headers)
            for transaction in Transactions.all():
                order = Orders.get(id=transaction.order_transaction.value)
                values = [
                    str(transaction.id.value),
                    User.get(user_id=order.user.value).username.value,
                    str(transaction.created.value),
                    f"ord-{transaction.order_transaction.value}",
                    str(transaction.getAmount())
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])

        except Exception as e:
            # todo display message box
            print(self.__module__, e)

    def clearInputs(self):
        self._current_transaction_id = -1
        self.orders.setCurrentText("----------")
        self.created.setDateTime(QDateTime.currentDateTime())
        self.transactionId.clear()

    def cleaned_data(self) -> typing.Dict:
        self.error.clear()
        data = {'created': self.created.dateTime().toPyDateTime()}
        try:
            index = tuple(self._orders.values()).index(self.orders.currentText())
            data['order_transaction'] = tuple(self._orders.keys())[index]
        except Exception as e:
            self.error.setText("Invalid Order!!")
            return {}
        return data
