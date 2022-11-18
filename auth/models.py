import inspect
import typing
import hashlib
from db import models


class User(models.Model):
    username = models.CharacterField(max_length=20)
    password = models.PasswordField(max_length=20)
    first_name = models.CharacterField(max_length=20, null=True)
    last_name = models.CharacterField(max_length=20, null=True)
    email = models.EmailField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    def login(self):
        raise NotImplemented()

    def check_password(self, password: str) -> bool:
        _password = hashlib.sha256(password.encode()).hexdigest()
        return _password == self.password.value

    def _get_class_attrs(self) -> typing.Tuple[typing.Tuple[str, typing.Any]]:
        attributes = inspect.getmembers(User, lambda a: not (inspect.isroutine(a)) and not (inspect.isclass(a)))
        attributes = [attr for attr in attributes if not attr[0].startswith("_")]
        return tuple(attributes)
