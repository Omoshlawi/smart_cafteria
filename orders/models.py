from auth.models import User
from db import models
from food.models import Food


class Orders(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKeyField(User, on_delete=models.OnRelationShipModified.DELETE_CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)

    def getTotalCost(self):
        return sum([item.price.value for item in OrderItem.filter(order_id=self.id.value)])


class OrderItem(models.Model):
    id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    order_id = models.ForeignKeyField(Orders, related_name='items',
                                      on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    food = models.ForeignKeyField(Food, on_delete=models.OnRelationShipModified.DELETE_CASCADE,
                                  related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
