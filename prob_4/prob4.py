from csp import CSP, backtracking_search

def solve_crypto():
    letters = ['T', 'W', 'O', 'F', 'U', 'R']
    carries = ['C10', 'C100', 'C1000']
    variables = letters + carries

    domains = {}
    for letter in letters:
        domains[letter] = list(range(10))
    # T and F cannot be 0
    domains['T'] = list(range(1, 10))
    domains['F'] = list(range(1, 10))

    # carries are 0 or 1
    for carry in carries:
        domains[carry] = [0, 1]

    # Every variable is a neighbor to every other variable
    neighbors = {v: set() for v in variables}
    for v1 in variables:
        for v2 in variables:
            if v1 != v2:
                neighbors[v1].add(v2)
    neighbors = {k: list(v) for k, v in neighbors.items()}

    def constraint_fn(var1, val1, var2, val2, assignment):
        # AllDiff for letters
        if var1 in letters and var2 in letters:
            if val1 == val2:
                return False

        # Simulate adding var1=val1 to check global limits
        assignment[var1] = val1
        valid = True
        
        # Checking constraints
        if 'O' in assignment and 'R' in assignment and 'C10' in assignment:
            if assignment['O'] + assignment['O'] != assignment['R'] + 10 * assignment['C10']:
                valid = False

        if 'W' in assignment and 'U' in assignment and 'C10' in assignment and 'C100' in assignment:
            if assignment['W'] + assignment['W'] + assignment['C10'] != assignment['U'] + 10 * assignment['C100']:
                valid = False

        if 'T' in assignment and 'O' in assignment and 'C100' in assignment and 'C1000' in assignment:
            if assignment['T'] + assignment['T'] + assignment['C100'] != assignment['O'] + 10 * assignment['C1000']:
                valid = False

        if 'F' in assignment and 'C1000' in assignment:
            if assignment['F'] != assignment['C1000']:
                valid = False

        # Cleanup
        del assignment[var1]
        
        return valid

    csp = CSP(variables, domains, neighbors, constraint_fn)
    solution = backtracking_search(csp)

    print("--- Task 4: Cryptarithmetic Solution (TWO + TWO = FOUR) ---")
    if solution:
        for var in variables:
            print(f"{var} = {solution[var]}")
        print("\nEquation Check:")
        two = solution['T']*100 + solution['W']*10 + solution['O']
        four = solution['F']*1000 + solution['O']*100 + solution['U']*10 + solution['R']
        print(f"  {two}")
        print(f"+ {two}")
        print(f"-----")
        print(f" {four}")
    else:
        print("No solution found.")

if __name__ == '__main__':
    solve_crypto()
