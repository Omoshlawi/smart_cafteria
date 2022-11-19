import inspect
import typing

from db import models


class Food(models.Model):
    food_id = models.PositiveIntegerField(primary_key=True, auto_increment=True)

