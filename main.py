from auth.models import User
from food.models import Food
from students.models import Student
from db.sqlite import SqliteDb
# food = Food()
# print(food.get_class_attrs())
user = User.get(user_id=1)
user.username.setValue("Omosh")
user.save()
print(user)
# user.username.setValue("Omosh3")
# user.email.setValue('lawiomosh3@gmail.com')
# user.save()
# print(user.get_filed_name())
# print(user.get_class_attrs())
# stud = Student.create(registration_number="SCT221-116/2020", year_of_study=3)

# print(stud.get_class_attrs())
# SqliteDb.getDatabase().dropTable(user)
# SqliteDb.getDatabase().dropTable(stud)
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
