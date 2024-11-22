from src.utils import generate_data, write_schedule_to_csv
from src.data import DAYS, TIMESLOTS


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.number_of_steps = 0

    def is_consistent(self, assignment, variable, value, group_timeslots, teacher_assignments):
        time_slot, auditorium, teacher = value
        day, time = time_slot
        subject_name, group, lesson_type, iterator = variable

        for other_var, assigned_value in assignment.items():
            other_subject, other_group, _, _ = other_var
            assigned_time_slot, assigned_auditorium, assigned_teacher = assigned_value

            if assigned_time_slot == time_slot and assigned_teacher == teacher:  # same lecturer for assigned group
                return False
            if assigned_time_slot == time_slot and assigned_auditorium == auditorium:  # same auditorium for assigned group
                return False
        if group.number_of_students > auditorium.capacity:
            return False
        if time_slot in group_timeslots[group][day] or len(group_timeslots[group][day]) >= len(TIMESLOTS):  # group timeslot taken
            return False

        group_timeslots[group][day].add(time_slot)

        if teacher in teacher_assignments:
            assigned_time_slot, _ = teacher_assignments[teacher]
            if assigned_time_slot == time_slot:  # teacher taken
                return False

        teacher_assignments[teacher] = (time_slot, subject_name)

        return True

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment.keys()]

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

    def backtrack(self, assignment, group_timeslots, teacher_assignments):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(assignment, var):
            if self.is_consistent(assignment, var, value, group_timeslots, teacher_assignments):
                assignment[var] = value

                time_slot, auditorium, teacher = value
                day, time = time_slot
                subject_name, group, lesson_type, iterator = var

                result = self.backtrack(assignment, group_timeslots, teacher_assignments)
                if result is not None:
                    return result

                del assignment[var]
                group_timeslots[group][day].remove(time_slot)
                del teacher_assignments[teacher]

        return assignment

    def solve(self):
        groups = list(set([var[1] for var in self.variables]))

        assignment = {}
        group_timeslots = {group: {day: set() for day in DAYS} for group in groups}
        teacher_assignments = {}
        assignment = self.backtrack(assignment, group_timeslots, teacher_assignments)
        if len(assignment) == len(self.variables):
            print('Solution is full')
        return assignment


variables, domains, constraints = generate_data()
csp_solver = CSP(variables, domains, constraints)
schedule = csp_solver.solve()
write_schedule_to_csv(schedule)
