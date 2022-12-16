import os
import sys

from PyQt6.QtWidgets import QApplication

from auth.view import LoginView
from settings import RESOURCES


def run():
    # db = SqliteDb.getDatabase()
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
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
