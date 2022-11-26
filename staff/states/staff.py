from typing import cast

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QDateEdit

from auth.models import User
from staff.models import Staff
from staff.states.base import BaseManager
from utils.utilities import template


class StaffManager(BaseManager):
    def __init__(self):
        super(StaffManager, self).__init__(QWidget(), template("staffManager.ui"))
        self.firstName = cast(QLineEdit, self.window.findChild(QLineEdit, 'firstName'))
        self.lastName = cast(QLineEdit, self.window.findChild(QLineEdit, 'lastName'))
        self.email = cast(QLineEdit, self.window.findChild(QLineEdit, 'email'))
        self.staffId = cast(QLineEdit, self.window.findChild(QLineEdit, 'staffId'))
        self.role = cast(QLineEdit, self.window.findChild(QLineEdit, 'role'))
        self.dateOfEmployment = cast(QDateEdit, self.window.findChild(QDateEdit, 'dateOfEmployment'))
        self.addStaff = cast(QPushButton, self.window.findChild(QPushButton, 'addStaff'))
        self.updateStaff = cast(QPushButton, self.window.findChild(QPushButton, 'updateStaff'))
        self.deleteStaff = cast(QPushButton, self.window.findChild(QPushButton, 'deleteStaff'))
        self.resetCredentials = cast(QPushButton, self.window.findChild(QPushButton, 'resetCredentials'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.setUpStaffList()
        self.addEventListeners()

    def addEventListeners(self):
        self.addStaff.clicked.connect(self.handleAddStaff)

    def handleAddStaff(self):
        pass

    def setUpStaffList(self):
        self.treeView.clear()
        staffs = Staff.all()
        self.treeView.setColumnCount(5)
        self.treeView.setSortingEnabled(True)
        headers = [
            'id',
            'Staff Number',
            'First Name',
            'Last Name',
            'Date of Employment',
            'Email',
            'Role'
        ]
        self.treeView.setHeaderLabels(headers)

        for staff in staffs:
            try:
                user = User.get(user_id=staff.user.value)
                values = [
                    str(user.user_id.value),
                    staffs.staff_id.value,
                    user.first_name.value,
                    user.last_name.value,
                    str(staff.date_of_employment.value),
                    user.email.value,
                    staff.course.value
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
            except Exception as e:
                # todo display error in messagebox
                print(e, "here")
