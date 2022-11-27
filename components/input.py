from PyQt6.QtWidgets import QLineEdit


class CustomLineEdit(QLineEdit):
    def __init__(self, food:dict):
        super(CustomLineEdit, self).__init__()
        self.food = food['food_name']
        self.price = food['unit_price']
        self.setPlaceholderText(str(self.food) + ": @Ksh." + str(self.price))

    def setCustomText(self, quantity):
        total_price = quantity * self.price
        self.setText("Ksh. " + str(total_price))

    def set_default_price(self):
        self.setText("Ksh. " + str(self.price))