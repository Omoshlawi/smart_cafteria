import typing

from db.models import Model
import inspect
from datetime import datetime

from db.models import Model


class Student(Model):
    registration_number: str = ""
    year_of_study: datetime = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        attributes = inspect.getmembers(Student, lambda a: not (inspect.isroutine(a)) and not (inspect.isclass(a)))
        attributes = [attr for attr in attributes if not attr[0].startswith("_")]
        return tuple(attributes)

