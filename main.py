from auth.models import User
from db import models
from students.models import Student
from students.view import MainWindow
user = User(username="Omosh", last_name='12')
# ui = MainWindow()
# f = models.BooleanField(default=True)
# f.setValue("hellow@gmail.com")
print([getattr(user, f) for f in user.get_filed_name()])
