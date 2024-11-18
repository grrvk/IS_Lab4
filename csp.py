class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

        self.number_of_steps = 0

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

    def forward_checking(self, assignment, variable, value):
        domains_copy = {var: list(domain) for var, domain in self.domains.items()}

        for var in self.constraints[variable]:
            if var not in assignment and value in domains_copy[var]:
                domains_copy[var].remove(value)

        for var in self.constraints[variable]:
            if var not in assignment and len(domains_copy[var]) == 0:
                return False, None

        return True, domains_copy

    def is_consistent(self, assignment, variable, value):
        for var in self.constraints[variable]:
            if var in assignment and assignment[var] == value:
                return False
        return True

    def is_full(self, assignment):
        if len(assignment) == len(self.variables):
            print('Solution is full and satisfies all constraints\n')
        else:
            print('Solution is not full\n')

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(assignment, var):
            if self.is_consistent(assignment, var, value):
                assignment[var] = value
                self.number_of_steps += 1

                original_domains = self.domains.copy()

                status, domains = self.forward_checking(assignment, var, value)
                if status:
                    self.domains = domains
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result

                self.domains = original_domains
                del assignment[var]

        return None

    def solve(self):
        assignment = {}
        assignment = self.backtrack(assignment)
        self.is_full(assignment)
        return assignment
