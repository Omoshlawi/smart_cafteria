from db.models import Model
from datetime import datetime


class Student(Model):
    registration_number: str = ""
    year_of_study: datetime = None
