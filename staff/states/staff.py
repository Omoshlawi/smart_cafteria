import typing
from datetime import date
from typing import cast

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QDateEdit, \
    QLabel, QMessageBox

from auth.models import User
from components.creds_form import CredentialsForm
from staff.models import Staff
from staff.states.base import BaseManager
from utils.utilities import template


class StaffManager(BaseManager):
    def __init__(self):
        super(StaffManager, self).__init__(QWidget(), template("staffManager.ui"))
        self._user_Id = -1
        self.firstName = cast(QLineEdit, self.window.findChild(QLineEdit, 'firstName'))
        self.lastName = cast(QLineEdit, self.window.findChild(QLineEdit, 'lastName'))
        self.email = cast(QLineEdit, self.window.findChild(QLineEdit, 'email'))
        self.staffId = cast(QLineEdit, self.window.findChild(QLineEdit, 'staffId'))
        self.role = cast(QLineEdit, self.window.findChild(QLineEdit, 'role'))
        self.salary = cast(QLineEdit, self.window.findChild(QLineEdit, 'salary'))
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
        self.deleteStaff.clicked.connect(self.handleDeleteStaff)
        self.updateStaff.clicked.connect(self.handleUpdateStaff)
        self.treeView.itemDoubleClicked.connect(self.onDoubleClickItem)

    def onDoubleClickItem(self, item):
        id_ = int(item.text(0))
        self._user_Id = id_
        user = User.get(user_id=id_)
        data = user.toJson()
        staff = Staff.get(user=id_)
        data.update(staff.toJson())
        self.populateData(data)

    def populateData(self, data):
        try:
            self.firstName.setText(data['first_name'])
            self.lastName.setText(data['last_name'])
            self.email.setText(data['email'])
            self.role.setText(data['role'])
            self.staffId.setText(data['staff_id'])
            self.dateOfEmployment.setDate(date.fromisoformat(data['date_of_employment']))
            self.salary.setText(str(data['salary']))
        except Exception as e:
            # TODO handle data appropriately
            print(e)

    def clearInputs(self):
        self._user_Id = -1
        self.firstName.clear()
        self.lastName.clear()
        self.email.clear()
        self.staffId.clear()
        self.role.clear()
        self.salary.clear()

    def handleUpdateStaff(self):
        cd = self.cleaned_data()
        if cd and self._user_Id != -1:
            try:
                user = User.get(
                    user_id=self._user_Id
                )
                user.username.setValue(cd['staffId']),
                user.email.setValue(cd['email']),
                user.first_name.setValue(cd['firstName']),
                user.last_name.setValue(cd['lastName']),
                user.save()
                staff = Staff.get(
                    user=self._user_Id
                )
                staff.staff_id.setValue(cd['staffId']),
                staff.date_of_employment.setValue(cd['dateOfEmployment']),
                staff.role.setValue(cd['role']),
                staff.salary.setValue(cd['salary'])
                staff.save()
                self.setUpStaffList()
                self.clearInputs()
            except Exception as e:
                # TODO THROW ERROR IN MESSAGEBOX
                print(self.__module__, e)

    def handleDeleteStaff(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            user = User.get(user_id=id_)
            staff = Staff.get(user=id_)
            dlg = QMessageBox(self.window)
            dlg.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
            dlg.setWindowTitle("Warning!!")
            dlg.setText(f"Are you sure you want to delete '{user.get_full_name()}'\n"
                        f"This operation will permanently delete the record")
            status = dlg.exec()
            if status == QMessageBox.StandardButton.Apply:
                user.delete()
                staff.delete()
                self.setUpStaffList()

    def handleSetCredentials(self):
        curr_item = self.treeView.currentItem()
        if curr_item:
            id_ = int(curr_item.text(0))
            user = User.get(user_id=id_)
            self.credsDialog = CredentialsForm(user.toJson(), self.window)
            self.credsDialog.exec()

    def handleAddStaff(self):
        cd = self.cleaned_data()
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
                    role=cd['role'],
                    salary=cd['salary']
                )
                self.setUpStaffList()
                self.clearInputs()
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
        try:
            d = float(self.salary.text())
            data['salary'] = d
        except ValueError:
            self.error.setText("Enter valid employee salary")
            self.salary.setFocus()

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
