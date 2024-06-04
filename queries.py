from sqlalchemy import func, desc

from models import Student, Group, Lecturer, Subject, Grade, session


def select_1():
    # Znajdź 5 uczniów z najwyższymi wynikami GPA ze wszystkich przedmiotów.
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Grade) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5) \
        .all()


def select_2(subject_name):
    # Znajdź ucznia z najwyższą oceną średnią z danego przedmiotu.
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Grade) \
        .join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .first()


def select_3(subject_name):
    # Znajdź średni wynik w grupach z określonego przedmiotu.
    return session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Subject) \
        .filter(Subject.name == subject_name) \
        .scalar()


def select_4():
    # Znajdź średni wynik w transmisji (w całej tabeli wyników).
    return session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).scalar()


def select_5(lecturer_name):
    # Dowiedz się, jakich zajęć uczy dany nauczyciel.
    return session.query(Subject.name) \
        .join(Lecturer) \
        .filter(Lecturer.fullname == lecturer_name) \
        .all()


def select_6(group_name):
    # Znajdź listę uczniów w określonej grupie.
    return session.query(Student.fullname) \
        .join(Group) \
        .filter(Group.name == group_name) \
        .all()


def select_7(group_name, subject_name):
    # Znajdź oceny uczniów w osobnej grupie dla konkretnego przedmiotu.
    return session.query(Student.fullname, Grade.grade) \
        .join(Grade) \
        .join(Subject) \
        .join(Group) \
        .filter(Group.name == group_name, Subject.name == subject_name) \
        .all()


def select_8(lecturer_name):
    # Znajdź średni wynik uzyskany przez określonego nauczyciela z jego przedmiotów.
    return session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Subject) \
        .join(Lecturer) \
        .filter(Lecturer.fullname == lecturer_name) \
        .scalar()


def select_9(student_name):
    # Znajdź listę kursów, w których uczestniczy dany student.
    return session.query(Subject.name) \
        .join(Grade) \
        .join(Student) \
        .filter(Student.fullname == student_name) \
        .all()


def select_10(student_name, lecturer_name):
    # Lista kursów prowadzonych dla konkretnego ucznia przez określonego nauczyciela.
    return session.query(Subject.name) \
        .join(Grade) \
        .join(Student) \
        .join(Lecturer) \
        .filter(Student.fullname == student_name, Lecturer.fullname == lecturer_name) \
        .all()


# Przykładowe wywołania funkcji
if __name__ == "__main__":
    print("1. 5 uczniów z najwyższymi wynikami GPA ze wszystkich przedmiotów:")
    print(select_1())

    print("\n2. Uczeń z najwyższą oceną średnią z przedmiotu Matematyka:")
    print(select_2('Math'))

    print("\n3. Średni wynik w grupach dla przedmiotu Fizyka:")
    print(select_3('Physics'))

    print("\n4. Średni wynik w transmisji (w całej tabeli wyników):")
    print(select_4())

    print("\n5. Zajęcia, które prowadzi nauczyciel o nazwisku John Doe:")
    print(select_5('John Doe'))

    print("\n6. Lista uczniów w grupie Group A:")
    print(select_6('Group A'))

    print("\n7. Oceny uczniów w grupie Group A dla przedmiotu Math:")
    print(select_7('Group A', 'Math'))

    print("\n8. Średni wynik uzyskany przez nauczyciela John Doe z jego przedmiotów:")
    print(select_8('John Doe'))

    print("\n9. Lista kursów, w których uczestniczy student John Smith:")
    print(select_9('John Smith'))

    print("\n10. Lista kursów prowadzonych dla ucznia John Smith przez nauczyciela John Doe:")
    print(select_10('John Smith', 'John Doe'))
