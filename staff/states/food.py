import typing
from decimal import Decimal, InvalidOperation
from typing import cast

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QLineEdit, QCheckBox, QPushButton, QLabel, \
    QTreeWidgetItem

from food.models import Food
from staff.states.base import BaseManager
from utils.utilities import template


class FoodManager(BaseManager):
    def __init__(self):
        super(FoodManager, self).__init__(QWidget(), template("foodsManager.ui"))
        self.food = cast(QLineEdit, self.window.findChild(QLineEdit, 'food'))
        self.unitPrice = cast(QLineEdit, self.window.findChild(QLineEdit, 'unitPrice'))
        self.available = cast(QCheckBox, self.window.findChild(QCheckBox, 'available'))
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self._food_id = -1
        self.addFood = cast(QPushButton, self.window.findChild(QPushButton, 'addFood'))
        self.updateFood = cast(QPushButton, self.window.findChild(QPushButton, 'updateFood'))
        self.deleteFood = cast(QPushButton, self.window.findChild(QPushButton, 'deleteFood'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.setUpFoodList()
        self.addEventListeners()

    def addEventListeners(self):
        self.addFood.clicked.connect(self.handleAddFood)
        self.treeView.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.updateFood.clicked.connect(self.handleFoodUpdate)
        self.deleteFood.clicked.connect(self.handleFoodDelete)

    def handleFoodDelete(self):
        pass

    def handleFoodUpdate(self):
        cd = self.cleaned_data()
        if cd and self._food_id != -1:
            try:
                print(cd)
                food = Food.get(food_id=self._food_id)
                print(food.toJson())
                food.food_name.setValue(cd['food'])
                food.unit_price.setValue(float(cd['unitPrice']))
                food.available.setValue(cd['available'])
                food.save()
                self.setUpFoodList()
                self.clearInputs()
            except Exception as e:
                print(self.__module__, e)

    def onItemDoubleClicked(self, item):
        id_ = int(item.text(0))
        self._food_id = id_
        food = Food.get(food_id=id_)
        data = food.toJson()
        self.populateFields(data)

    def populateFields(self, data):
        self.food.setText(data['food_name'])
        self.unitPrice.setText(str(data['unit_price']))
        self.available.setChecked(data['available'] == 1)

    def handleAddFood(self):
        cd = self.cleaned_data()
        if cd:
            try:
                Food.create(
                    food_name=cd['food'],
                    unit_price=float(cd['unitPrice']),
                    available=cd['available']
                )
                self.clearInputs()
                self.setUpFoodList()
            except Exception as e:
                print(self.__module__, e)

    def clearInputs(self):
        self._food_id = -1
        self.food.clear()
        self.available.setChecked(False)
        self.unitPrice.clear()

    def setUpFoodList(self):
        self.treeView.clear()
        try:
            foods = Food.all()
            self.treeView.setColumnCount(4)
            self.treeView.setSortingEnabled(True)
            headers = [
                'id',
                'Availability',
                'Food',
                'Unit Price'
            ]
            self.treeView.setHeaderLabels(headers)
            for food in foods:
                values = [
                    str(food.food_id.value),
                    "Available" if food.available.value else "Unavailable",
                    food.food_name.value,
                    str(food.unit_price.value)
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
        except Exception as e:
            # todo display message box
            print(self.__module__, e)

    def cleaned_data(self) -> typing.Dict:
        data = {}
        if not self.food.text():
            self.error.setText("Please Enter Food name")
            self.food.setFocus()
            return {}
        else:
            data['food'] = self.food.text()
        try:
            p = Decimal(self.unitPrice.text())
            data['unitPrice'] = p
        except InvalidOperation:
            self.error.setText("Please Enter food unit price")
            self.unitPrice.setFocus()
            return {}
        data['available'] = self.available.isChecked()
        return data
