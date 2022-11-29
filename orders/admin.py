import typing
from typing import cast

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QWidget, QLineEdit, QDateTimeEdit, QComboBox, QCheckBox, QPushButton, QVBoxLayout, \
    QTreeWidget, QTreeWidgetItem, QLabel, QMessageBox

from auth.models import User
from orders.models import Orders
from staff.states.base import BaseManager
from utils.utilities import template


class OrderAdmin(BaseManager):
    def __init__(self):
        super(OrderAdmin, self).__init__(QWidget(), template("orderManager.ui"))
        self._users = {user.user_id.value: user.username.value for user in User.all()}
        self.orderId = cast(QLineEdit, self.window.findChild(QLineEdit, 'orderId'))
        self.created = cast(QDateTimeEdit, self.window.findChild(QDateTimeEdit, 'created'))
        self.created.setDateTime(QDateTime.currentDateTime())
        self.orderUser = cast(QComboBox, self.window.findChild(QComboBox, 'user'))
        self.paid = cast(QCheckBox, self.window.findChild(QCheckBox, 'paid'))
        self.addOrder = cast(QPushButton, self.window.findChild(QPushButton, 'addOrder'))
        self.updateOrder = cast(QPushButton, self.window.findChild(QPushButton, 'updateOrder'))
        self.deleteOrder = cast(QPushButton, self.window.findChild(QPushButton, 'deleteOrder'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self._current_order_id = -1
        self.fillComboBox()
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.setUpOrdersList()
        self.addEventHandlers()

    def fillComboBox(self):
        # if self._update:
        self.orderUser.addItems(self._users.values())
        self.orderUser.setCurrentText('-------------------')

    def addEventHandlers(self):
        self.addOrder.clicked.connect(self.handleAddOrder)
        self.updateOrder.clicked.connect(self.handleUpdateOrder)
        self.treeView.itemDoubleClicked.connect(self.onOrderDoubleClicked)
        self.deleteOrder.clicked.connect(self.handleDeleteOrder)

    def handleDeleteOrder(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            order = Orders.get(id=id_)
            dlg = QMessageBox(self.window)
            dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
            dlg.setWindowTitle("Warning!!")
            dlg.setText(f"Are you sure you want to delete Order-'{order.id.value}'\n"
                        f"This operation will permanently delete the record")
            status = dlg.exec()
            if status == QMessageBox.StandardButton.Apply:
                order.delete()
                self.setUpOrdersList()
                self.clearInputs()

    def onOrderDoubleClicked(self, item):
        id_ = int(item.text(0))
        self._current_order_id = id_
        order = Orders.get(id=id_)
        self.populateFields(order.toJson())

    def populateFields(self, data):
        try:
            self.orderId.setText(str(data['id']))
            self.created.setDateTime(self.created.dateTimeFromText(data['created']))
            self.paid.setChecked(data['paid'] == 1)
            self.orderUser.setCurrentText(str(User.get(user_id=data['user'])))
        except Exception as e:
            print(e)

    def clearInputs(self):
        self._current_order_id = -1
        self.orderUser.setCurrentText("----------")
        self.created.setDateTime(QDateTime.currentDateTime())
        self.paid.setChecked(False)
        self.orderId.clear()

    def handleUpdateOrder(self):
        cd = self.cleaned_data()
        if cd and self._current_order_id != -1:
            order = Orders.get(id=self._current_order_id)
            order.paid.setValue(cd['paid'])
            order.created.setValue(cd['created'])
            order.user.setValue(cd['user'])
            order.save()
            self.setUpOrdersList()
            self.clearInputs()

    def handleAddOrder(self):
        cd = self.cleaned_data()
        if cd:
            Orders.create(
                user=cd['user'],
                created=cd['created'],
                paid=cd['paid']
            )
            self.setUpOrdersList()

    def cleaned_data(self) -> typing.Dict:
        # print(self.created.dateTimeFromText(self.created.text()))
        data = {'created': self.created.dateTime().toPyDateTime()}
        try:
            index = tuple(self._users.values()).index(self.orderUser.currentText())
            data['user'] = tuple(self._users.keys())[index]
        except Exception as e:
            self.error.setText("Invalid User!!")
            return {}
        data['paid'] = self.paid.isChecked()
        return data

    def setUpOrdersList(self):
        self.treeView.clear()
        try:
            self.treeView.setColumnCount(4)
            self.treeView.setSortingEnabled(True)
            headers = [
                'id',
                'Created',
                'User',
                'Status'
            ]
            self.treeView.setHeaderLabels(headers)
            for order in Orders.all():
                values = [
                    str(order.id.value),
                    str(order.created.value),
                    str(order.user.value),
                    "Paid" if order.paid.value else "Pending",
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
        except Exception as e:
            # todo display message box
            print(self.__module__, e)
