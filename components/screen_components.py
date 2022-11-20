from PyQt6.QtGui import QPixmap


class Logo(QPixmap):
    def __init__(self, length, width, src):
        super().__init__()
        self.scaled(width, length)
        self.load(src)
