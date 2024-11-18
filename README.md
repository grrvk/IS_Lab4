# CLS sudoku solving

## Puzzle generation

Generate random full sudoku puzzle 9x9 and the remove some values to create a problem to solve

```
full_puzzle = generate_puzzle()
puzzle = remove_cells(full_puzzle)
print_grid(puzzle)
```

## Puzzle solving

Initialize variables, domains and constraints, then CLS class, run solve method and print the result

```
variables, domains, constraints = generate_data(puzzle)
csp = CSP(variables, domains, constraints)
solution = csp.solve()
solution_grid = generate_grid(solution)
print_grid(solution_grid)
```