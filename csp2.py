from utils2 import generate_data, write_schedule_to_csv


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.number_of_steps = 0

    def is_consistent(self, assignment, variable, value, group_day_count, group_timeslots, teacher_assignments):
        """
        Check if the assignment of a variable value is consistent with the current assignment.
        Includes checks for:
        - Group-day limit: No more than 3 lessons for the same group per day.
        - No other lesson for the same group at the same time.
        - No teacher assigned to multiple subjects at the same time.
        - No other group assigned to the same subject at the same time.
        """
        # Extract information from the variable and the value
        time_slot, auditorium, teacher = value
        day, time = time_slot
        subject_name, group, lesson_type = variable

        # Check if there is already a subject in the same timeslot for another group
        for other_var, assigned_value in assignment.items():
            other_subject, other_group, _ = other_var
            assigned_time_slot, assigned_auditorium, assigned_teacher = assigned_value

            # Check for teacher conflict: Same timeslot and the same teacher assigned to another group
            if assigned_time_slot == time_slot and assigned_teacher == teacher:
                if other_group != group:
                    return False  # The same lecturer is assigned to another group in the same timeslot
                if other_subject == subject_name:
                    return False  # The same subject is already assigned to another group in the same timeslot

            # Check for auditorium conflict: Same timeslot and the same auditorium for different groups
            if assigned_time_slot == time_slot and assigned_auditorium == auditorium:
                if other_group != group:  # Different group in the same auditorium at the same time
                    return False  # The auditorium is already occupied by another group at the same time
        # The same subject is already assigned to another group in the same timeslot

        # Group-day constraint: Ensure no more than 3 lessons for the same group on the same day
        if group not in group_day_count:
            group_day_count[group] = {}

        if day not in group_day_count[group]:
            group_day_count[group][day] = 0

        if group_day_count[group][day] >= 3:
            return False  # More than 3 lessons for the group on the same day

        # Update group-day lesson count
        group_day_count[group][day] += 1

        # Check if the group already has a lesson at the same timeslot on the same day
        if group not in group_timeslots:
            group_timeslots[group] = {}

        if day not in group_timeslots[group]:
            group_timeslots[group][day] = set()

        if time_slot in group_timeslots[group][day]:
            return False  # Group already has a lesson at the same time

        # Update the timeslot assignment for the group
        group_timeslots[group][day].add(time_slot)

        # Check if the teacher is already assigned to another subject at the same timeslot
        if teacher in teacher_assignments:
            assigned_time_slot, _ = teacher_assignments[teacher]
            if assigned_time_slot == time_slot:
                return False  # Teacher is already assigned to another subject in the same timeslot

        # Update teacher assignment to prevent double booking
        teacher_assignments[teacher] = (time_slot, subject_name)

        return True

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]

        if len(unassigned_vars) == 0:
            return None

        def min_remaining(uv):
            minimal_remained_len = min(len(self.domains[var]) for var in uv)
            return [var for var in uv if len(self.domains[var]) == minimal_remained_len]

        minimal_remaining_vars = min_remaining(unassigned_vars)
        if len(minimal_remaining_vars) == 1:
            return minimal_remaining_vars[0]

        def max_degree(uv):
            variable_degree = {}
            for var in uv:
                variable_degree[var] = 0
                lookup_vars = [c_var for c_var in uv if c_var != var]
                for lookup_var in lookup_vars:
                    for elem in self.constraints[lookup_var]:
                        if elem == var:
                            variable_degree[var] += 1
            sorted_by_degree = dict(sorted(variable_degree.items(), key=lambda item: item[1], reverse=True))
            return next(iter(sorted_by_degree))

        max_constraint_var = max_degree(minimal_remaining_vars)
        return max_constraint_var

    def order_domain_values(self, assignment, variable):
        def count_constraints(value):
            constraints_removed = 0
            for var in self.constraints[variable]:
                if var not in assignment and value in self.domains[var]:
                    constraints_removed += 1
            return constraints_removed

        variable_values = self.domains[variable].copy()
        constraints_count = {v: count_constraints(v) for v in variable_values}
        return constraints_count.keys()

    def forward_checking(self, assignment, variable, value, group_day_count, group_timeslots, teacher_assignments):
        domains_copy = {var: list(domain) for var, domain in self.domains.items()}

        for var in self.constraints[variable]:
            if var not in assignment and value in domains_copy[var]:
                domains_copy[var].remove(value)

        for var in self.constraints[variable]:
            if var not in assignment and len(domains_copy[var]) == 0:
                return False, None

        return True, domains_copy

    def backtrack(self, assignment, group_day_count, group_timeslots, teacher_assignments):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        print(f'Assignment: {len(assignment)}, Variable: {var}')

        for value in self.order_domain_values(assignment, var):
            if self.is_consistent(assignment, var, value, group_day_count, group_timeslots, teacher_assignments):
                assignment[var] = value

                # Update the helper dictionaries
                time_slot, auditorium, teacher = value
                day, time = time_slot
                subject_name, group, lesson_type = var

                # Update teacher_assignments
                teacher_assignments[teacher] = (time_slot, subject_name)

                # Forward checking and recursive call
                result = self.backtrack(assignment, group_day_count, group_timeslots, teacher_assignments)
                if result is not None:
                    return result

                # Undo the changes made during this iteration
                del assignment[var]

                # Undo updates to group_day_count
                group_day_count[group][day] -= 1

                # Undo updates to group_timeslots
                group_timeslots[group][day].remove(time_slot)

                # Undo updates to teacher_assignments
                del teacher_assignments[teacher]

        return assignment

    def solve(self):
        assignment = {}
        group_day_count = {}  # Initialize group_day_count to track the number of lessons per day per group
        group_timeslots = {}  # Initialize group_timeslots to track the assigned timeslots for each group
        teacher_assignments = {}  # Initialize teacher_assignments to track teachers' current assignments
        assignment = self.backtrack(assignment, group_day_count, group_timeslots, teacher_assignments)
        print(group_day_count)
        print(f'Assignment: {len(assignment)}, variables: {len(self.variables)}')
        return assignment


# Example usage:
variables, domains, constraints = generate_data()  # Get the variables, domains, and constraints from generate_data()
csp_solver = CSP(variables, domains, constraints)
schedule = csp_solver.solve()

write_schedule_to_csv(schedule)

# Print the schedule
# if schedule:
#     for lesson, (time_slot, auditorium, teacher) in schedule.items():
#         print(
#             f"Lesson: {lesson[0]}, Group: {lesson[1]}, Type: {lesson[2]}, Time: {time_slot}, Auditorium: {auditorium}, Teacher: {teacher}")
