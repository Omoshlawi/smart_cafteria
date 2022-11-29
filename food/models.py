from db import models


class Food(models.Model):
    food_id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    food_name = models.CharacterField(max_length=20, unique=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    available = models.BooleanField(default=False)

    def __str__(self):
        return str(self.food_name.value)
