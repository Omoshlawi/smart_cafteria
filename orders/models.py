from auth.models import User
from db import models
from food.models import Food


class Order(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKeyField(User, on_delete=models.OnRelationShipModified.DELETE_CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKeyField(Order, related_name='items', on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    product = models.ForeignKeyField(Food, on_delete=models.OnRelationShipModified.DELETE_CASCADE,
                                     related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
