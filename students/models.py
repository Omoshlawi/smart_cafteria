import inspect
import typing

from auth.models import User
from db import models
from db.models import Model


class Student(Model):
    user = models.OneToOneField(
        User,
        on_delete=models.OnRelationShipModified.DELETE_CASCADE,
        related_name="students"
    )
    registration_number = models.CharacterField(max_length=20, unique=True, index=True)
    year_of_study = models.PositiveIntegerField()
    course = models.CharacterField(max_length=255, null=True)

