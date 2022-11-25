import os
import sys
from db.models import BooleanField
from PyQt6.QtWidgets import QApplication
from db.models import BooleanField
from auth.models import User
from auth.view import LoginView
from db.sqlite import SqliteDb
from settings import RESOURCES
from students.models import Student


def run():
    # u = User.get(user_id = 1)
    # print(u)

    # db = SqliteDb.getDatabase()
    # s = Student()
    # u = User()
    # db.dropTable(s)
    # db.dropTable(u)
    # db.close()
    # User.create(
    #     username="admin",
    #     password="admin",
    #     email="admin@admin.com",
    #     first_name="Admin",
    #     last_name="Super",
    #     is_staff=True,
    #     is_admin=True
    # )
    app = QApplication(sys.argv)
    app.setStyle('FUSION')
    with open(os.path.join(RESOURCES, 'qss', 'styles.qss'), 'rt') as f:
        app.setStyleSheet(f.read())
    ui = LoginView()
    ui.window.show()
    # student = Student.get(user=1)
    # print(student.registration_number)
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
