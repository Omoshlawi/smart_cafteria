import datetime
import os
import sys

from PyQt6.QtWidgets import QApplication

from auth.models import User
from auth.view import LoginView
from db.models import DateField, ForeignKeyField, DateTimeField, PositiveIntegerField, BooleanField, OneToOneField, OnRelationShipModified
from db.sqlite import SqliteDb
from orders.models import Orders
from settings import RESOURCES, BASE_DIR
from students.models import Student


def run():
    db = SqliteDb.getDatabase()
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
