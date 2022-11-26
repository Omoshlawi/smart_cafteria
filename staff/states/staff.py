import typing
from typing import cast

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QDateEdit, \
    QLabel

from auth.models import User
from components.creds_form import CredentialsForm
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
        self.error = cast(QLabel, self.window.findChild(QLabel, 'error'))
        self.treeContainer = cast(QVBoxLayout, self.window.findChild(QVBoxLayout, 'treeContainer'))
        self.treeView = QTreeWidget()
        self.treeContainer.addWidget(self.treeView)
        self.setUpStaffList()
        self.addEventListeners()

    def addEventListeners(self):
        self.addStaff.clicked.connect(self.handleAddStaff)
        self.resetCredentials.clicked.connect(self.handleSetCredentials)

    def handleSetCredentials(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            user = User.get(user_id=id_)
            self.credsDialog = CredentialsForm(user.toJson(), self.window)
            self.credsDialog.exec()

    def handleAddStaff(self):
        cd = self.cleaned_data()
        print(str(cd['dateOfEmployment']))
        if cd:
            try:
                user = User.create(
                    username=cd['staffId'],
                    email=cd['email'],
                    first_name=cd['firstName'],
                    last_name=cd['lastName'],
                    password=cd['staffId'],
                    is_staff=True
                )
                staff = Staff.create(
                    user=user.user_id.value,
                    staff_id=cd['staffId'],
                    date_of_employment=cd['dateOfEmployment'],
                    role=cd['role']
                )
                self.setUpStaffList()
            except Exception as e:
                # TODO THROW ERROR IN MESSAGEBOX
                print(self.__module__, e)

    def cleaned_data(self) -> typing.Dict:
        data = {}
        if not self.firstName.text():
            self.error.setText("Please Enter first name")
            self.firstName.setFocus()
            return {}
        else:
            data['firstName'] = self.firstName.text()
        if not self.lastName.text():
            self.error.setText("Please enter staff last name")
            self.lastName.setFocus()
            return {}
        else:
            data['lastName'] = self.lastName.text()
        if not self.email.text():
            self.error.setText("Please enter staff email")
            self.email.setFocus()
            return {}
        else:
            data['email'] = self.email.text()
        if not self.staffId.text():
            self.error.setText("Please enter staff Number")
            self.staffId.setFocus()
            return {}
        else:
            data['staffId'] = self.staffId.text()

        data['dateOfEmployment'] = self.dateOfEmployment.date().toPyDate()
        if not self.role.text():
            self.error.setText("Please enter staffs role")
            self.role.setFocus()
            return {}
        else:
            data['role'] = self.role.text()
        return data

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
                    staff.staff_id.value,
                    user.first_name.value,
                    user.last_name.value,
                    str(staff.date_of_employment.value),
                    user.email.value,
                    staff.role.value
                ]
                self.treeView.addTopLevelItems([QTreeWidgetItem(values)])
            except Exception as e:
                # todo display error in messagebox
                print(self.__module__, 'setUpStaffList', e)
