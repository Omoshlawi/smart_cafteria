from db.manager import Manager
from db.models import Model


class User(Model):
    username: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    is_active: bool = False
    is_staff: bool = False
    is_admin: bool = False

    def login(self):
        raise NotImplemented()

    def check_password(self, password: str) -> bool:
        raise NotImplemented()
