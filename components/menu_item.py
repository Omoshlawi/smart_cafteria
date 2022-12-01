from PyQt6.QtWidgets import QCheckBox, QLabel, QLineEdit

from components.quantasizer import QuantaSizer


class MenuItem:
    def __init__(self, food, updateTotal):
        self.updateTotal = updateTotal
        self._food = food.toJson()
        self._meal = QCheckBox()
        self._meal.setText(self._food['food_name'])
        self._price = QLabel(str(self._food['unit_price']))
        self._total_cost = QLineEdit(str(0))
        self._total_cost.setReadOnly(True)
        self._quantaSizer = QuantaSizer(
            onValueChanged=self.onQuantityChanged
        )

        self._handleMealToggled(self._meal.isChecked())
        self._addEventListeners()

    def onQuantityChanged(self, value):
        self._total_cost.setText(
            str(value * float(self._price.text()))
        )

    def _addEventListeners(self):
        self._meal.toggled.connect(self._handleMealToggled)
        self._total_cost.textChanged.connect(self.updateTotal)

    def _handleMealToggled(self, checked):
        self._quantaSizer.setEnabled(checked)
        if not checked:
            self._total_cost.setText("0")

    def __str__(self):
        return str({
            'Food': self._food['food_name'],
            'Quantity': self._quantaSizer.text,
            'Price': self._food['unit_price'],
            'Total': self._total_cost.text()
        })

    def __repr__(self):
        return self.__str__()

    @property
    def mealId(self):
        return self._food['food_id']

    @property
    def selected(self) -> bool:
        return self.meal.isChecked()

    @property
    def buyable(self) -> bool:
        return self._meal.isChecked() and int(self.quantaSizer.text) > 0

    @property
    def meal(self):
        return self._meal

    @property
    def quantaSizer(self):
        return self._quantaSizer

    @property
    def price(self):
        return self._price

    @property
    def totalCost(self):
        return self._total_cost
