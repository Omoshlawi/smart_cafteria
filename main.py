import sys
import os
from PyQt6.QtWidgets import QApplication

from cafteria.views import MainWindow
from settings import RESOURCES


def run():
    app = QApplication(sys.argv)
    app.setStyle('FUSION')
    print(os.path.join(RESOURCES, 'images', 'vstec_green.png'))
    # ./images/vstec_green.png)
    with open(os.path.join(RESOURCES, 'qss', 'styles.qss'), 'rt') as f:
        app.setStyleSheet(f.read())
    main = MainWindow()
    main.window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
