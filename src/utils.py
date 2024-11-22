import csv
from src.data import SUBJECTS, AUDITORIUMS, TEACHERS, TIMESLOTS, DAYS


def getValidTeacher(subject_name, lesson_type):
    valid_subject_teachers = [teacher for teacher in TEACHERS if subject_name in teacher.subject_taught]
    valid_subject_teachers = [teacher for teacher in valid_subject_teachers if lesson_type in teacher.subject_type]
    return valid_subject_teachers


def generate_data():
    variables = []
    domains = {}
    constraints = {}

    for subject in SUBJECTS:
        for i in range(subject.lectures_number):
            variables.append((subject.subject_name, subject.group, 'Лекція', i))
        for i in range(subject.practice_number):
            variables.append((subject.subject_name, subject.group, 'Практика', i))

    timeslots = [(day, time) for day in DAYS for time in TIMESLOTS]

    for variable in variables:
        subject_name, group, lesson_type, iterator = variable
        suitable_teachers = getValidTeacher(subject_name, lesson_type)
        domains[variable] = [
            (time_slot, auditorium, teacher)
            for time_slot in timeslots
            for auditorium in AUDITORIUMS
            for teacher in suitable_teachers
        ]

        constraints[variable] = []

        for other_variable in variables:
            if variable == other_variable:
                continue
            other_subject_name, other_group, _, _ = other_variable

            if group == other_group:
                constraints[variable].append(other_variable)
            if subject_name == other_subject_name:
                constraints[variable].append(other_variable)

    return variables, domains, constraints


def write_schedule_to_csv(assignment, filename="schedule.csv"):

    sorted_assignment = sorted(
        assignment.items(),
        key=lambda item: (
            DAYS.index(item[1][0][0]),
            TIMESLOTS.index(item[1][0][1])
        )
    )

    rows = []
    for (subject, group, lesson_type, i), (time_slot, auditorium, teacher) in sorted_assignment:
        day, time = time_slot
        rows.append([subject, group, lesson_type, day, time, auditorium, teacher.name])

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Group', 'Lesson Type', 'Day', 'Time', 'Auditorium', 'Teacher'])
        writer.writerows(rows)

    print(f"Schedule successfully written to {filename}")