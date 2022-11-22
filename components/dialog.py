from enum import Enum

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

from core.exceptions import InvalidArgumentError
from db.models import Model


class InputDialogBoxPurpose(Enum):
    CREATE = 0
    UPDATE = 1



class InputDialogBox(QDialog):
    def __init__(self, parent, instance: Model, purpose, title="cafeteria"):
        super().__init__(parent)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.setModal(True)
        self.lineEdits = []
        self.baseLayout = QFormLayout()
        self.setLayout(self.baseLayout)
        self.setWindowTitle(title)
        self._instance = instance
        self._purpose = purpose
        self.fields = list(self._instance.get_filed_name())
        self.fields.remove(self._instance.getPk())
        self.renderWindow()
        self.addEventListeners()

    def renderWindow(self):
        if self._purpose == InputDialogBoxPurpose.CREATE:
            for field in self.fields:
                edit = QLineEdit()
                self.baseLayout.addRow(" ".join(str(field).capitalize().split('_')), edit)
                self.lineEdits.append(edit)
        elif self._purpose == InputDialogBoxPurpose.UPDATE:
            for field in self.fields:
                edit = QLineEdit()
                self.baseLayout.addRow(" ".join(str(field).capitalize().split('_')), QLineEdit())
                self.lineEdits.append(edit)
        else:
            raise InvalidArgumentError()
        self.baseLayout.addRow(self.buttonBox)

    def getInputs(self):
        values = [val.text() for val in self.lineEdits]
        kwargs = dict(zip(self.fields, values))
        if self._purpose == InputDialogBoxPurpose.CREATE:
            for key in kwargs:
                setattr(self._instance, key, getattr(self._instance, key).setValue(kwargs[key]))
                self._instance.save()
        elif self._purpose == InputDialogBoxPurpose.UPDATE:
            pass
        self.accept()

    def addEventListeners(self):
        self.buttonBox.accepted.connect(self.getInputs)
        # self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
