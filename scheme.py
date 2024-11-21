import itertools


class Group:
    def __init__(self, group_name, number_of_students):
        self.group_name = group_name
        self.number_of_students = number_of_students

    def __repr__(self):
        return f"{self.group_name}"


class Teacher:
    def __init__(self, name, subject_taught, subject_types, maxHoursPerWeek):
        self.name = name
        self.subject_taught = subject_taught
        self.subject_type = subject_types
        self.maxHoursPerWeek = maxHoursPerWeek

        self.occupied_hours = 0

    def __repr__(self):
        return f"{self.name}"


class Auditorium:
    def __init__(self, auditorium_name, capacity):
        self.auditorium_name = auditorium_name
        self.capacity = capacity

    def __repr__(self):
        return f"{self.auditorium_name}"


class Subject:
    def __init__(self, subject_name, group, lectures_number, practice_number):
        self.subject_name = subject_name
        self.group = group
        self.lectures_number = lectures_number
        self.practice_number = practice_number

    def __repr__(self):
        return (f"{self.subject_name}")


class Lesson:
    id_iter = itertools.count()

    def __init__(self, subject, subject_type, group, teacher):
        self.id = next(self.id_iter)
        self.subject = subject
        self.subject_type = subject_type
        self.group = group
        self.teacher = teacher

        self.hours_occupied = 0

    def __repr__(self):
        return (f"Lesson {self.subject}, {self.subject_type}, {self.group}, "
                f"{self.teacher}")



