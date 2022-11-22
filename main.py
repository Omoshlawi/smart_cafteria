import os
import sys

from PyQt6.QtWidgets import QApplication

from auth.models import User
from auth.view import LoginView
from cafteria.views import MainWindow
from students.view import StudentsView
from settings import RESOURCES


def run():
    app = QApplication(sys.argv)
    app.setStyle('FUSION')
    with open(os.path.join(RESOURCES, 'qss', 'styles.qss'), 'rt') as f:
        app.setStyleSheet(f.read())
    ui = LoginView()
    ui.window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
