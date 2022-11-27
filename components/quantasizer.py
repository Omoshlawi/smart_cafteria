from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLineEdit


class QuantaSizer(QWidget):
    def __init__(self, parent=None, initial=0, step=1, max_=20, onValueChanged=None):
        super().__init__(parent=parent)
        self._onValueChanged = onValueChanged
        self._step = step
        self._max = max_
        self._initial = initial
        self._layout = QHBoxLayout()
        self._minus = QPushButton("-")
        self._plus = QPushButton("+")
        self._value = QLineEdit(str(self._initial))
        self._value.setReadOnly(True)
        self._layout.addWidget(self._minus)
        self._layout.addWidget(self._value)
        self._layout.addWidget(self._plus)
        self.setLayout(self._layout)
        self._addEventHandlers()

    def _addEventHandlers(self):
        self._plus.clicked.connect(self._handlePlus)
        self._minus.clicked.connect(self._handleMinus)

    def _handlePlus(self):
        if self._initial < self._max:
            self._initial += self._step
            self._value.setText(str(self._initial))
            if self._onValueChanged is not None:
                self._onValueChanged(self._initial)

    def _handleMinus(self):
        if self._initial > 0:
            self._initial -= self._step
            self._value.setText(str(self._initial))
            if self._onValueChanged is not None:
                self._onValueChanged(self._initial)

    def reset(self):
        self._value.setText(str(0))

    def setEnabled(self, a0: bool) -> None:
        super(QuantaSizer, self).setEnabled(a0)
        self.reset()

    @property
    def text(self):
        return self._value.text()
