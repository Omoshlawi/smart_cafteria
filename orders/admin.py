import typing
from typing import cast

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QWidget, QLineEdit, QDateTimeEdit, QComboBox, QCheckBox, QPushButton, QVBoxLayout, \
    QTreeWidget, QTreeWidgetItem, QLabel, QMessageBox, QDialog, QSpinBox

from auth.models import User
from food.models import Food
from orders.models import Orders, OrderItem
from staff.states.base import BaseManager
from utils.utilities import template
from view.generics import View


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
        self.orderItems = cast(QPushButton, self.window.findChild(QPushButton, 'orderItems'))
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
        self.orderItems.clicked.connect(self.handleOrderItems)

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

    def handleOrderItems(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            order = Orders.get(id=id_)
            dlg = OrderItemsView(order)
            status = dlg.exec()
            if status:
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
            # todo decide wether tho remove me or not
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
            try:
                Orders.create(
                    user=cd['user'],
                    created=cd['created'],
                    paid=cd['paid']
                )
                self.setUpOrdersList()
            except Exception as e:
                self.error.setText(str(e))

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
                'Status',
                'Items',
                'Amount'
            ]
            self.treeView.setHeaderLabels(headers)
            for order in Orders.all():
                values = [
                    str(order.id.value),
                    str(order.created.value),
                    str(order.user.value),
                    "Paid" if order.paid.value else "Pending",
                    str(len(tuple(OrderItem.filter(order_id=order.id.value)))),
                    str(order.getTotalCost())
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])

        except Exception as e:
            # todo display message box
            print(self.__module__, e)


class OrderItemsView(View):
    def __init__(self, order, parent=None):
        self._order_dict = order.toJson()
        super().__init__(QDialog(parent=None), template("orderItemsManagerForm.ui"))
        self._foods = {food.food_id.value: food.food_name.value for food in Food.all()}
        self._currentOrderItem = -1
        self.window = cast(QDialog, self.window)
        self.window.setModal(True)
        self.window.setWindowTitle("OrderItems")
        self.itemsTreeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'itemsTreeContainer'))
        self.treeView = QTreeWidget()
        self.itemId = cast(QLineEdit, self.window.findChild(QLineEdit, 'itemId'))
        self.foodCombo = cast(QComboBox, self.window.findChild(QComboBox, 'food'))
        self.quantity = cast(QSpinBox, self.window.findChild(QSpinBox, 'quantity'))
        self.apply = cast(QPushButton, self.window.findChild(QPushButton, 'apply'))
        self.cancel = cast(QPushButton, self.window.findChild(QPushButton, 'cancel'))
        self.addItem = cast(QPushButton, self.window.findChild(QPushButton, 'addItem'))
        self.updateItem = cast(QPushButton, self.window.findChild(QPushButton, 'updateItem'))
        self.deleteItem = cast(QPushButton, self.window.findChild(QPushButton, 'deleteItem'))
        self.deleteAllItems = cast(QPushButton, self.window.findChild(QPushButton, 'deleteAllItems'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self.orderId = cast(QLabel, self.window.findChild(QLabel, 'orderId'))
        self.orderId.setText(f"Order-{self._order_dict['id']}")
        self.fillComboBox()
        self.itemsTreeContainer.addWidget(self.treeView)
        self.addEventHandlers()
        self.setUpOrderItemsList()

    def fillComboBox(self):
        # if self._update:
        self.foodCombo.addItems(self._foods.values())
        self.foodCombo.setCurrentText('-------------------')

    def setUpOrderItemsList(self):
        self.treeView.clear()
        try:
            self.treeView.setColumnCount(5)
            self.treeView.setSortingEnabled(True)
            headers = [
                'id',
                'Food',
                'Unit Price',
                'Quantity',
                'Total Price'
            ]
            self.treeView.setHeaderLabels(headers)
            for item in OrderItem.filter(order_id=self._order_dict['id']):
                food = Food.get(food_id=item.food.value)
                values = [
                    str(item.id.value),
                    str(food),
                    str(food.unit_price.value),
                    str(item.quantity.value),
                    str(item.getTotalPrice())
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
        except Exception as e:
            # todo display message box
            print(self.__module__, e)

    def addEventHandlers(self):
        self.addItem.clicked.connect(self.handleAddItem)
        self.updateItem.clicked.connect(self.handleItemUpdate)
        self.deleteItem.clicked.connect(self.handleItemDelete)
        self.deleteAllItems.clicked.connect(self.handleDeleteAllItems)
        self.apply.clicked.connect(self.window.accept)
        self.cancel.clicked.connect(self.window.reject)
        self.treeView.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def handleItemDelete(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            order_item = OrderItem.get(id=id_)
            dlg = QMessageBox(self.window)
            dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
            dlg.setWindowTitle("Warning!!")
            dlg.setText(f"Are you sure you want to delete Item-'{Food.get(food_id=order_item.food.value)}'\n"
                        f"This operation will permanently delete the record")
            status = dlg.exec()
            if status == QMessageBox.StandardButton.Apply:
                order_item.delete()
                self.setUpOrderItemsList()
                self.clearInputs()

    def handleDeleteAllItems(self):
        dlg = QMessageBox(self.window)
        dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
        dlg.setWindowTitle("Warning!!")
        dlg.setText(f"Are you sure you want to delete all order Items\n"
                    f"This operation will permanently delete the record")
        status = dlg.exec()
        if status == QMessageBox.StandardButton.Apply:
            for item in OrderItem.filter(order_id=self._order_dict['id']):
                item.delete()
            self.setUpOrderItemsList()
            self.clearInputs()

    def handleItemUpdate(self):
        cd = self.cleaned_data()
        if cd and self._currentOrderItem != -1:
            try:
                item = OrderItem.get(id=self._currentOrderItem)
                item.food.setValue(cd['food'])
                item.quantity.setValue(cd['quantity'])
                item.save()
                self.setUpOrderItemsList()
                self.clearInputs()
            except Exception as e:
                self.error.setText(str(e))

    def onItemDoubleClicked(self, item):
        id_ = int(item.text(0))
        self._currentOrderItem = id_
        order_item = OrderItem.get(id=id_)
        self.populateFields(order_item.toJson())

    def populateFields(self, data):
        try:
            self.itemId.setText(str(data['id']))
            self.foodCombo.setCurrentText(str(Food.get(food_id=data['food'])))
            self.quantity.setValue(data['quantity'])
        except Exception as e:
            # todo decide wether tho remove me or not
            print(e)

    def handleAddItem(self):
        cd = self.cleaned_data()
        if cd:
            try:
                OrderItem.create(
                    order_id=self._order_dict['id'],
                    food=cd['food'],
                    quantity=cd['quantity'],
                )
                self.setUpOrderItemsList()
                self.clearInputs()
            except Exception as e:
                self.error.setText(str(e))

    def exec(self):
        return self.window.exec()

    def clearInputs(self):
        self._currentOrderItem = -1
        self.foodCombo.setCurrentText("----------")
        self.quantity.setValue(0)
        pass

    def cleaned_data(self) -> typing.Dict:
        # print(self.created.dateTimeFromText(self.created.text()))
        self.error.clear()
        data = {}
        try:
            index = tuple(self._foods.values()).index(self.foodCombo.currentText())
            data['food'] = tuple(self._foods.keys())[index]
        except Exception as e:
            self.error.setText("Invalid Food!!")
            return {}
        if not isinstance(self.quantity.value(), int) or self.quantity.value() < 1:
            self.error.setText("The quantity must not be less than one")
            return {}
        else:
            data['quantity'] = self.quantity.value()
        return data
