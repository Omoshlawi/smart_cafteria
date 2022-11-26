from auth.models import User
from db import models


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    staff_id = models.CharacterField(max_length=25)
    role = models.TextField()
    salary = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    date_of_employment = models.DateTimeField()
