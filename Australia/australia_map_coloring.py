"""
Australia Map Coloring — Constraint Satisfaction Problem (CSP)
==============================================================
Assigns one of three colors to each of Australia's 7 states/territories
such that no two neighboring regions share the same color.

Algorithm: Backtracking Search with:
  - Minimum Remaining Values (MRV) heuristic
  - Degree heuristic (tie-breaker)
  - Forward Checking (constraint propagation)
  - Least Constraining Value (LCV) ordering
"""

from copy import deepcopy


# ── 1. PROBLEM DEFINITION ────────────────────────────────────────────────────

REGIONS = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]

NEIGHBORS = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "Q"],
    "SA":  ["WA", "NT", "Q", "NSW", "V"],
    "Q":   ["NT", "SA", "NSW"],
    "NSW": ["Q",  "SA", "V"],
    "V":   ["SA", "NSW"],
    "T":   []                      # Tasmania — island, no land neighbors
}

COLORS = ["Red", "Green", "Blue"]


# ── 2. CONSTRAINT CHECK ──────────────────────────────────────────────────────

def is_consistent(region, color, assignment):
    """
    Return True if assigning `color` to `region` violates no constraint.
    A constraint is violated when a neighbor already has the same color.
    """
    for neighbor in NEIGHBORS[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True


# ── 3. FORWARD CHECKING ──────────────────────────────────────────────────────

def forward_check(region, color, domains):
    """
    After assigning `color` to `region`, prune that color from every
    unassigned neighbor's domain.

    Returns (updated_domains, list_of_pruned_pairs) so we can restore
    domains on backtrack.  Returns (None, _) if any neighbor's domain
    becomes empty (dead end detected early).
    """
    pruned = []
    new_domains = deepcopy(domains)

    for neighbor in NEIGHBORS[region]:
        if color in new_domains[neighbor]:
            new_domains[neighbor].remove(color)
            pruned.append((neighbor, color))
            if not new_domains[neighbor]:          # domain wipe-out → backtrack
                return None, pruned

    return new_domains, pruned


# ── 4. VARIABLE ORDERING — MRV + DEGREE ──────────────────────────────────────

def select_unassigned_variable(assignment, domains):
    """
    Minimum Remaining Values (MRV): pick the unassigned variable with the
    fewest legal colors left — fail fast.

    Degree heuristic (tie-breaker): among MRV ties, prefer the variable
    involved in the most constraints with *unassigned* neighbors.
    """
    unassigned = [r for r in REGIONS if r not in assignment]

    # MRV
    min_domain = min(len(domains[r]) for r in unassigned)
    mrv_vars   = [r for r in unassigned if len(domains[r]) == min_domain]

    if len(mrv_vars) == 1:
        return mrv_vars[0]

    # Degree tie-break
    def degree(r):
        return sum(1 for n in NEIGHBORS[r] if n not in assignment)

    return max(mrv_vars, key=degree)


# ── 5. VALUE ORDERING — LEAST CONSTRAINING VALUE ─────────────────────────────

def order_domain_values(region, domains, assignment):
    """
    Least Constraining Value (LCV): prefer the color that rules out the
    fewest choices for unassigned neighbors — leaves the most freedom.
    """
    def conflict_count(color):
        count = 0
        for neighbor in NEIGHBORS[region]:
            if neighbor not in assignment and color in domains[neighbor]:
                count += 1
        return count

    return sorted(domains[region], key=conflict_count)


# ── 6. BACKTRACKING SEARCH ───────────────────────────────────────────────────

def backtrack(assignment, domains, stats):
    """
    Recursive backtracking search.

    `stats` is a dict we pass around to count attempts and backtracks
    for educational output.
    """
    if len(assignment) == len(REGIONS):          # all regions colored → done
        return assignment

    region = select_unassigned_variable(assignment, domains)
    stats["calls"] += 1

    print(f"\n  Trying region: {region:4s}  |  domain: {domains[region]}")

    for color in order_domain_values(region, domains, assignment):
        if is_consistent(region, color, assignment):
            assignment[region] = color
            print(f"    ✓ Assign {region} = {color}")

            new_domains, pruned = forward_check(region, color, domains)

            if new_domains is not None:          # no domain wipe-out
                result = backtrack(assignment, new_domains, stats)
                if result is not None:
                    return result

            # Failure — undo assignment and restore domains
            del assignment[region]
            stats["backtracks"] += 1
            print(f"    ✗ Backtrack from {region} = {color}")

    return None                                  # no solution found from here


# ── 7. SOLVER ENTRY POINT ────────────────────────────────────────────────────

def solve_map_coloring():
    # Each region starts with all three colors available
    initial_domains = {region: list(COLORS) for region in REGIONS}

    assignment = {}
    stats      = {"calls": 0, "backtracks": 0}

    print("=" * 60)
    print("   Australia Map Coloring — CSP with Backtracking")
    print("=" * 60)
    print(f"\nRegions  : {REGIONS}")
    print(f"Colors   : {COLORS}")
    print(f"\nAdjacency list:")
    for r, nbrs in NEIGHBORS.items():
        print(f"  {r:5s} → {nbrs if nbrs else ['(none — island)']}")

    print("\n── Search trace ─────────────────────────────────────")

    solution = backtrack(assignment, initial_domains, stats)

    print("\n" + "=" * 60)

    if solution:
        print("  SOLUTION FOUND")
        print("=" * 60)

        # Pretty table
        col_w = 12
        header = f"  {'Region':<10} {'Color':<10} {'Neighbors'}"
        print(header)
        print("  " + "-" * 50)

        for region in REGIONS:
            color     = solution[region]
            neighbors = NEIGHBORS[region] or ["(none)"]
            nbr_str   = ", ".join(
                f"{n}={solution[n]}" for n in neighbors if n in solution
            ) or "—"
            print(f"  {region:<10} {color:<10} {nbr_str}")

        print("\n── Constraint verification ───────────────────────────")
        all_ok = True
        for region in REGIONS:
            for neighbor in NEIGHBORS[region]:
                if solution[region] == solution[neighbor]:
                    print(f"  ✗ CONFLICT: {region} and {neighbor} both = {solution[region]}")
                    all_ok = False
        if all_ok:
            print("  ✓ All constraints satisfied — no adjacent regions share a color.")

        print(f"\n── Search statistics ─────────────────────────────────")
        print(f"  Recursive calls : {stats['calls']}")
        print(f"  Backtracks      : {stats['backtracks']}")

    else:
        print("  NO SOLUTION EXISTS (unexpected for this problem).")

    print("=" * 60)
    return solution


# ── 8. BONUS: CONSTRAINT GRAPH SUMMARY ───────────────────────────────────────

def print_constraint_graph():
    print("\n── Constraint graph (unique edges) ──────────────────────")
    seen = set()
    for r, nbrs in NEIGHBORS.items():
        for n in nbrs:
            edge = tuple(sorted([r, n]))
            if edge not in seen:
                seen.add(edge)
                print(f"  {edge[0]} ── {edge[1]}")
    print(f"\n  Total constraints (edges): {len(seen)}")
    print(f"  Total variables          : {len(REGIONS)}")
    print(f"  Domain size per variable : {len(COLORS)}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    solution = solve_map_coloring()
    print_constraint_graph()
