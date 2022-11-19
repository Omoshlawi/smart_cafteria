import hashlib
import inspect
import typing
from datetime import datetime
from db import models


class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True, auto_increment=True)
    username = models.CharacterField(max_length=20)
    password = models.PasswordField(max_length=20)
    first_name = models.CharacterField(max_length=20, null=True)
    last_name = models.CharacterField(max_length=20, null=True)
    email = models.EmailField(max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return str(self.username)

    def __repr__(self):
        return str(self)

    def login(self):
        raise NotImplemented()

    def check_password(self, password: str) -> bool:
        _password = hashlib.sha256(password.encode()).hexdigest()
        return _password == self.password.value

