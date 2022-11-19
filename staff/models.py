from auth.models import User
from db import models


class Staff(models.Model):
    staff_id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    user = models.OneToOneField(User, on_delete=models.OnRelationShipModified.DELETE_CASCADE)
    role = models.TextField()