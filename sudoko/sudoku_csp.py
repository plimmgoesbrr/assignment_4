"""
Sudoku Puzzle Solver using CSP (Constraint Satisfaction Problem)
Algorithm: Backtracking + Forward Checking + MRV + AC-3 Arc Consistency
Reference: AIMA Section 5.2.6
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. CSP FORMULATION
#    Variables  : 81 cells (row 0-8, col 0-8)
#    Domain     : {1..9} (reduced to given digit for pre-filled cells)
#    Constraints:
#      - All cells in the same ROW must be different
#      - All cells in the same COLUMN must be different
#      - All cells in the same 3×3 BOX must be different
# ─────────────────────────────────────────────────────────────────────────────

import copy
import time

# ── Helpers ──────────────────────────────────────────────────────────────────

def cell(r, c):
    return r * 9 + c

def peers(pos):
    """Return all cells that share a row, column, or 3×3 box with `pos`."""
    r, c = divmod(pos, 9)
    row_peers  = {cell(r, j)          for j in range(9) if j != c}
    col_peers  = {cell(i, c)          for i in range(9) if i != r}
    br, bc     = (r // 3) * 3, (c // 3) * 3
    box_peers  = {cell(br + dr, bc + dc)
                  for dr in range(3) for dc in range(3)
                  if (br + dr, bc + dc) != (r, c)}
    return row_peers | col_peers | box_peers

# Pre-compute peer sets for all 81 cells
PEERS = [peers(i) for i in range(81)]

# ── AC-3 Arc Consistency ──────────────────────────────────────────────────────

def ac3(domains):
    """
    Enforce arc consistency across the entire grid.
    Returns False if a domain becomes empty (contradiction).
    """
    queue = [(xi, xj) for xi in range(81) for xj in PEERS[xi]]
    while queue:
        xi, xj = queue.pop()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in PEERS[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    """Remove values from domains[xi] that have no support in domains[xj]."""
    revised = False
    for val in list(domains[xi]):
        if all(val == v for v in domains[xj]):
            domains[xi].discard(val)
            revised = True
    return revised

# ── MRV Variable Selection ────────────────────────────────────────────────────

def select_unassigned(assignment, domains):
    """Pick the unassigned cell with the smallest remaining domain (MRV)."""
    unassigned = [i for i in range(81) if i not in assignment]
    return min(unassigned, key=lambda i: len(domains[i]))

# ── Forward Checking ──────────────────────────────────────────────────────────

def forward_check(pos, value, domains):
    """
    Remove `value` from peer domains after assigning it to `pos`.
    Returns (success, pruned) where pruned records what was removed for undo.
    """
    pruned = {}
    for peer in PEERS[pos]:
        if value in domains[peer]:
            domains[peer].discard(value)
            pruned.setdefault(peer, set()).add(value)
            if not domains[peer]:
                return False, pruned
    return True, pruned

def undo_pruning(pruned, domains):
    for peer, values in pruned.items():
        domains[peer] |= values

# ── Backtracking Search ───────────────────────────────────────────────────────

def backtrack(assignment, domains):
    if len(assignment) == 81:
        return assignment

    pos = select_unassigned(assignment, domains)

    for value in sorted(domains[pos]):
        assignment[pos] = value
        ok, pruned = forward_check(pos, value, domains)
        if ok:
            result = backtrack(assignment, domains)
            if result is not None:
                return result
        undo_pruning(pruned, domains)
        del assignment[pos]

    return None

# ── Main Solve Function ───────────────────────────────────────────────────────

def solve(puzzle):
    """
    puzzle: list of 81 ints, 0 = empty cell.
    Returns solved grid as list of 81 ints, or None if unsolvable.
    """
    # Initialise domains
    domains = [set(range(1, 10)) if puzzle[i] == 0 else {puzzle[i]}
               for i in range(81)]

    # Pre-assign givens into assignment dict
    assignment = {i: puzzle[i] for i in range(81) if puzzle[i] != 0}

    # Propagate givens via AC-3
    if not ac3(domains):
        return None

    result = backtrack(assignment, domains)
    if result is None:
        return None
    return [result[i] for i in range(81)]

# ─────────────────────────────────────────────────────────────────────────────
# 2. DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

def print_grid(grid, title="", highlight=None):
    h_top  = "┌───────┬───────┬───────┐"
    h_mid  = "├───────┼───────┼───────┤"
    h_bot  = "└───────┴───────┴───────┘"

    print(f"\n{BOLD}{title}{RESET}" if title else "")
    print(h_top)
    for r in range(9):
        if r in (3, 6):
            print(h_mid)
        row_str = "│"
        for c in range(9):
            val = grid[r * 9 + c]
            if c in (3, 6):
                row_str += "│"
            if val == 0:
                row_str += f" {DIM}·{RESET}"
            elif highlight and (r * 9 + c) in highlight:
                row_str += f" {CYAN}{val}{RESET}"
            else:
                row_str += f" {YELLOW}{val}{RESET}"
        row_str += " │"
        print(row_str)
    print(h_bot)

# ─────────────────────────────────────────────────────────────────────────────
# 3. SAMPLE PUZZLES
# ─────────────────────────────────────────────────────────────────────────────

# Each puzzle is a string of 81 chars, '0' = empty
PUZZLES = {
    "Easy": (
        "530070000"
        "600195000"
        "098000060"
        "800060003"
        "400803001"
        "700020006"
        "060000280"
        "000419005"
        "000080079"
    ),
    "Medium": (
        "000000907"
        "000420180"
        "000705026"
        "100904000"
        "050000040"
        "000507009"
        "920108000"
        "034059000"
        "507000000"
    ),
    "Hard": (
        "000000010"
        "400000000"
        "020000000"
        "000050407"
        "008000300"
        "001090000"
        "300400200"
        "050100000"
        "000806000"
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def run_puzzle(name, puzzle_str):
    puzzle = [int(ch) for ch in puzzle_str]
    given  = {i for i, v in enumerate(puzzle) if v != 0}

    print(f"\n{'═'*35}")
    print(f"  Puzzle: {name}")
    print(f"{'═'*35}")
    print_grid(puzzle, title="  Initial Board:")

    t0  = time.time()
    sol = solve(puzzle)
    t1  = time.time()

    if sol:
        solved_cells = {i for i in range(81) if i not in given}
        print_grid(sol, title="  Solved Board:", highlight=solved_cells)
        print(f"\n  {BOLD}✓ Solved in {(t1-t0)*1000:.1f} ms{RESET}")
    else:
        print(f"\n  ✗ No solution found.")

if __name__ == "__main__":
    print(f"\n{BOLD}{'═'*35}")
    print("  Sudoku Solver — CSP")
    print(f"  Backtracking + FC + MRV + AC-3")
    print(f"{'═'*35}{RESET}")

    for name, puzzle_str in PUZZLES.items():
        run_puzzle(name, puzzle_str)
