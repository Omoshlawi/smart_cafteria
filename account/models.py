from db import models
from students.models import Student


class Account(models.Model):
    student = models.OneToOneField(Student, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)


class Transaction(models.Model):
    pass