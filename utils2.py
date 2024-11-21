import random
import csv
from data import GROUPS, SUBJECTS, AUDITORIUMS, TEACHERS, TIMESLOTS, DAYS
from scheme import Lesson


def getValidTeacher(subject_name, lesson_type):
    valid_subject_teachers = [teacher for teacher in TEACHERS if subject_name in teacher.subject_taught]
    valid_subject_teachers = [teacher for teacher in valid_subject_teachers if lesson_type in teacher.subject_type]
    return valid_subject_teachers


def generate_data():
    variables = []  # Each variable: (subject_name, group, lesson_type)
    domains = {}    # Domains contain tuples: (time_slot, auditorium, teacher)
    constraints = {}  # Constraint dictionary for each variable

    for subject in SUBJECTS:
        for _ in range(subject.lectures_number):
            variables.append((subject.subject_name, subject.group, 'Лекція'))
        for _ in range(subject.practice_number):
            variables.append((subject.subject_name, subject.group, 'Практика'))

    timeslots = [(day, time) for day in DAYS for time in TIMESLOTS]

    for variable in variables:
        subject_name, group, lesson_type = variable
        suitable_teachers = getValidTeacher(subject_name, lesson_type)  # Assume this function is defined
        domains[variable] = [
            (time_slot, auditorium, teacher)
            for time_slot in timeslots
            for auditorium in AUDITORIUMS
            for teacher in suitable_teachers
        ]

        # Initialize empty constraints list for each variable
        constraints[variable] = []

        # Add constraints for the group and teacher conflicts
        for other_variable in variables:
            if variable == other_variable:
                continue  # Skip self-comparison
            other_subject_name, other_group, _ = other_variable

            if group == other_group:
                constraints[variable].append(other_variable)  # Same group constraint
            if subject_name == other_subject_name:
                constraints[variable].append(other_variable)  # Same subject constraint

        # Do not add 'group_day_limit' to constraints for domains, handle it logically during checking

    return variables, domains, constraints




def write_schedule_to_csv(assignment, filename="schedule.csv"):
    """
    Write the assignment (schedule) to a CSV file, sorted by index in DAYS and TIMESLOTS.
    """
    # Sort the assignment based on the index of day in DAYS and time in TIMESLOTS
    sorted_assignment = sorted(
        assignment.items(),
        key=lambda item: (
            DAYS.index(item[1][0][0]),  # Index of the day
            TIMESLOTS.index(item[1][0][1])  # Index of the time
        )
    )

    # Prepare the data for CSV writing
    rows = []
    for (subject, group, lesson_type), (time_slot, auditorium, teacher) in sorted_assignment:
        day, time = time_slot
        rows.append([subject, group, lesson_type, day, time, auditorium, teacher.name])

    # Write to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Group', 'Lesson Type', 'Day', 'Time', 'Auditorium', 'Teacher'])
        writer.writerows(rows)

    print(f"Schedule successfully written to {filename}")



# variables, domains, constraints = generate_data()
# print(constraints)