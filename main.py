from auth.models import User
from students.models import Student
from students.view import MainWindow
user = Student(registration_number="SCT221-116/2020", year_of_study=12)
# ui = MainWindow()
print(user)
