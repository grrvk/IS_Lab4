from csp import CSP
from utils import generate_grid, print_grid, generate_puzzle, remove_cells, generate_data, check_solution

print('Generating full sudoku puzzle and removing some cell values')
full_puzzle = generate_puzzle()
puzzle = remove_cells(full_puzzle)
print_grid(puzzle)

print('Initializing variables, domains, constraints')
variables, domains, constraints = generate_data(puzzle)

print('Solving puzzle')
csp = CSP(variables, domains, constraints)
solution = csp.solve()

print('Solution')
solution_grid = generate_grid(solution)
print_grid(solution_grid)
print(f'Solution is valid: {check_solution(solution_grid)}')
