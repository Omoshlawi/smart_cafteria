from auth.models import User
from db import models
from students.models import Student
from students.view import MainWindow
from utils.utilities import get_sql_fields

user = User.get(id_=7)
user.delete()
# print(user)
# user.save()
# ui = MainWindow()
# f = models.BooleanField(default=True)
# f.setValue("hellow@gmail.com")
# print(get_sql_fields(user))
# print([getattr(user, f) for f in user.get_filed_name()])
# print(user.check_password("jeff"))
