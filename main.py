from auth.models import User
from students.models import Student

user = Student(registration_number='sct221-0116/2929')

print(user.objects.all())
