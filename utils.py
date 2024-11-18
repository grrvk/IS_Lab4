from random import sample

BASE = 3


def generate_puzzle(base=BASE):
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % (base * base)

    def shuffle(s):
        return sample(s, len(s))

    base_range = range(base)
    rows = [g * base + r for g in shuffle(base_range) for r in shuffle(base_range)]
    cols = [g * base + c for g in shuffle(base_range) for c in shuffle(base_range)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board


def remove_cells(board, side=BASE*BASE, remove_rate=0.6):
    squares = side ** 2
    empties = int(squares * remove_rate)
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0
    return board


def generate_data(puzzle):
    def add_constraint(var):
        constraints_v = []
        for i in range(BASE*BASE):
            if i != var[0]:
                constraints_v.append((i, var[1]))
            if i != var[1]:
                constraints_v.append((var[0], i))

        sub_i, sub_j = var[0] // BASE, var[1] // BASE
        for i in range(sub_i * BASE, (sub_i + 1) * BASE):
            for j in range(sub_j * BASE, (sub_j + 1) * BASE):
                if (i, j) != var:
                    constraints_v.append((i, j))
        return constraints_v

    variables = [(i, j) for i in range(BASE*BASE) for j in range(BASE*BASE)]
    domains = {var: list(set(range(1, BASE*BASE+1))) if puzzle[var[0]][var[1]] == 0 else [puzzle[var[0]][var[1]]] for var in
               variables}

    constraints = {}
    for i in range(BASE*BASE):
        for j in range(BASE*BASE):
            constraints[(i, j)] = add_constraint((i, j))

    return variables, domains, constraints


def print_grid(solution):
    for i in range(BASE*BASE):
        if i % BASE == 0 and i != 0:
            print("- - - - - - - - - - - ")
        for j in range(BASE*BASE):
            if j % BASE == 0 and j != 0:
                print(" | ", end="")
            print(solution[i][j], end=" ")
        print()
    print('')


def generate_grid(solution):
    sol = [[0 for _ in range(BASE*BASE)] for _ in range(BASE*BASE)]
    for i in range(BASE*BASE):
        for j in range(BASE*BASE):
            if (i, j) in solution.keys():
                sol[i][j] = solution[i, j]
            else:
                sol[i][j] = 0
    return sol


def check_solution(solution):
    for row in solution:
        if sorted(row) != list(range(1, BASE*BASE+1)):
            return False

    for col in range(BASE*BASE):
        column = [solution[row][col] for row in range(BASE*BASE)]
        if sorted(column) != list(range(1, BASE*BASE+1)):
            return False

    for box_row in range(0, BASE*BASE, BASE):
        for box_col in range(0, BASE*BASE, BASE):
            square = [solution[row][col] for row in range(box_row, box_row + BASE) for col in range(box_col, box_col + BASE)]
            if sorted(square) != list(range(1, BASE*BASE+1)):
                return False

    return True
