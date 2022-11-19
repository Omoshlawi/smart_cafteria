from auth.models import User
from students.models import Student
from db.sqlite import SqliteDb
# SqliteDb.getDatabase().dropTable(User())
# SqliteDb.getDatabase().dropTable(Student())
# users = User.filter(username="Mother")
# for u in users:
#     print(u)

# user = User()
# stud = Student(registration_number="sct221-0116/2020", year_of_study=3)
# print(user.getIndexFields())
# print(user.user_id.pk)
# user.save()
# print(SqliteDb.get_sql_fields(user))
# print(user.get_valid_fields())
# print(users)
# user.save()
# ui = MainWindow()
# f = models.BooleanField(default=True)
# f.setValue("hellow@gmail.com")
# print(get_sql_fields(user))
# print([getattr(user, f) for f in user.get_filed_name()])
# print(user.check_password("jeff"))
