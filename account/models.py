from db import models
from orders.models import Orders
from students.models import Student


class Account(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    student = models.OneToOneField(Student, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    account = models.ForeignKeyField(Account, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    time = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKeyField(Orders, on_delete=models.OnRelationShipModified.DELETE_CASCADE, related_name="orders")
