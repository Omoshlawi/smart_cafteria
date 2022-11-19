import typing
from auth.models import User
from db import models
import inspect
from datetime import datetime

from db.models import Model


class Student(Model):
    user = models.OneToOneField(
        User,
        on_delete=models.OnRelationShipModified.DELETE_CASCADE,
        related_name="students"
    )
    registration_number = models.CharacterField(max_length=20, unique=True, index=True)
    year_of_study = models.PositiveIntegerField()
    kaka = models.ForeignKeyField(
        User,
        on_delete=models.OnRelationShipModified.DELETE_CASCADE,
        related_name="students"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        attributes = inspect.getmembers(Student, lambda a: not (inspect.isroutine(a)) and not (inspect.isclass(a)))
        attributes = [attr for attr in attributes if not attr[0].startswith("_")]
        return tuple(attributes)
