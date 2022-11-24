import typing

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


class StudentViewModel(QAbstractTableModel):
    def __init__(self, student=None):
        super().__init__()
        self.students = student or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            status, text = self.students(index.row())
            return text

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.students)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 6

