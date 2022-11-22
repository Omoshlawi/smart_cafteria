from PyQt6.QtWidgets import QWidget

from view.generics import View


class BaseManager(View):
    """
    Base state that defines the contractual resposibility of all state,
    It implements state pattern
    """
    def __init__(self, widget: QWidget, ui_file: str):
        super().__init__(widget, ui_file)

