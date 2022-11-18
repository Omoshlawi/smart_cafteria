from auth.models import User

users = User.filter(username="Mother")
for u in users:
    print(u)
# print(users)
# user.save()
# ui = MainWindow()
# f = models.BooleanField(default=True)
# f.setValue("hellow@gmail.com")
# print(get_sql_fields(user))
# print([getattr(user, f) for f in user.get_filed_name()])
# print(user.check_password("jeff"))
