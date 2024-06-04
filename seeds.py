from faker import Faker
import random
from models import Student, Group, Lecturer, Subject, Grade, session

# Tworzenie danych testowych za pomocą Faker
fake = Faker()

# Dodawanie studentów
for _ in range(random.randint(30, 50)):
    student = Student(fullname=fake.name())
    session.add(student)

# Dodawanie grup
groups = ['Group A', 'Group B', 'Group C']
group_objs = []
for group_name in groups:
    group = Group(name=group_name)
    session.add(group)
    group_objs.append(group)

# Dodawanie wykładowców
lecturers = []
for _ in range(random.randint(3, 5)):
    lecturer = Lecturer(fullname=fake.name())
    session.add(lecturer)
    lecturers.append(lecturer)

# Dodawanie przedmiotów i przypisywanie wykładowców
subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'Literature', 'Computer Science']
subject_objs = []
for subject_name in random.sample(subjects, random.randint(5, 8)):
    lecturer = random.choice(lecturers)
    subject = Subject(name=subject_name, lecturer=lecturer)
    session.add(subject)
    subject_objs.append(subject)

# Commit to add students, groups, lecturers, and subjects to the database
session.commit()

# Dodawanie ocen dla studentów
for student in session.query(Student).all():
    for subject in subject_objs:
        for _ in range(random.randint(0, 20)):
            grade = Grade(student=student, subject=subject, grade=random.randint(2, 5))
            session.add(grade)

# Zapisywanie zmian w bazie danych
session.commit()

print("Baza danych została pomyślnie wypełniona losowymi danymi.")
