from auth.models import User
from db import models
from orders.models import Orders


class Account(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    user = models.OneToOneField(User, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def debit(self, amount: float):
        self.balance.setValue(float(self.balance.value) - amount)

    def credit(self, amount: float):
        self.balance.setValue(float(self.balance.value) + amount)


class Transactions(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    created = models.DateTimeField(auto_now_add=True)
    order_transaction = models.ForeignKeyField(Orders, on_delete=models.OnRelationShipModified.DELETE_CASCADE,
                                               related_name="orders")

    def getAmount(self):
        order = Orders.get(id=self.order_transaction.value)
        return order.getTotalCost()
