# Australia Map Coloring — CSP

A classic **Constraint Satisfaction Problem (CSP)** solved with backtracking search, applied to coloring the 7 principal states and territories of Australia so that no two neighboring regions share the same color.

---

## Problem Statement

Given a map of Australia with 7 regions and a palette of 3 colors (**Red, Green, Blue**), assign a color to each region such that **no two adjacent regions have the same color**.

```
Regions : WA, NT, SA, Q (Queensland), NSW, V (Victoria), T (Tasmania)
Colors  : Red, Green, Blue
```

This is a textbook CSP from Russell & Norvig's *Artificial Intelligence: A Modern Approach*.

---

## Adjacency (Constraint Graph)

```
WA   ── NT
WA   ── SA
NT   ── SA
NT   ── Q
SA   ── Q
SA   ── NSW
SA   ── V
Q    ── NSW
NSW  ── V
T    ── (none — island, unconstrained)
```

Total constraints (edges): **9**

---

## Algorithm

### Core: Backtracking Search
A depth-first recursive search that:
1. **Assigns** a color to one region at a time.
2. **Checks consistency** — if the assignment violates a constraint, it **backtracks** immediately.
3. Repeats until all regions are colored or no solution exists.

### Optimization 1 — MRV (Minimum Remaining Values)
> *"Choose the variable with the fewest legal values left."*

Instead of picking regions in a fixed order, the solver always picks the region whose domain has been most pruned by previous assignments. This **fails fast** — dead ends are detected earlier, reducing wasted work.

### Optimization 2 — Degree Heuristic (MRV tie-breaker)
> *"Among tied MRV variables, prefer the one with the most constraints on remaining variables."*

When two regions have equal domain sizes, choose the one adjacent to the most unassigned neighbors. This tends to reduce future conflicts.

### Optimization 3 — Forward Checking (Constraint Propagation)
> *"After each assignment, immediately prune that color from all unassigned neighbors' domains."*

After coloring a region, the solver removes the used color from every neighbor's domain. If any neighbor's domain becomes **empty**, the current path is abandoned before even trying to assign it — avoiding wasted recursive calls.

### Optimization 4 — LCV (Least Constraining Value)
> *"Among legal colors for a region, try the one that eliminates the fewest choices for neighbors first."*

Values are sorted so the algorithm tries the "safest" option first — the color that leaves the most freedom for subsequent assignments.

---

## File Structure

```
australia_map_coloring.py   ← main solver (single file, no dependencies)
README.md
```

---

## Running the Code

**Requirements:** Python 3.7+ (standard library only — no pip install needed)

```bash
python australia_map_coloring.py
```

---

## Output

```
============================================================
   Australia Map Coloring — CSP with Backtracking
============================================================

Regions  : ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
Colors   : ['Red', 'Green', 'Blue']

Adjacency list:
  WA    → ['NT', 'SA']
  NT    → ['WA', 'SA', 'Q']
  SA    → ['WA', 'NT', 'Q', 'NSW', 'V']
  Q     → ['NT', 'SA', 'NSW']
  NSW   → ['Q', 'SA', 'V']
  V     → ['SA', 'NSW']
  T     → ['(none — island)']

── Search trace ─────────────────────────────────────

  Trying region: SA    |  domain: ['Red', 'Green', 'Blue']
    ✓ Assign SA = Red

  Trying region: NT    |  domain: ['Green', 'Blue']
    ✓ Assign NT = Green

  Trying region: Q     |  domain: ['Blue']
    ✓ Assign Q = Blue

  Trying region: NSW   |  domain: ['Green']
    ✓ Assign NSW = Green

  Trying region: WA    |  domain: ['Blue']
    ✓ Assign WA = Blue

  Trying region: V     |  domain: ['Blue']
    ✓ Assign V = Blue

  Trying region: T     |  domain: ['Red', 'Green', 'Blue']
    ✓ Assign T = Red

============================================================
  SOLUTION FOUND
============================================================
  Region     Color      Neighbors
  --------------------------------------------------
  WA         Blue       NT=Green, SA=Red
  NT         Green      WA=Blue, SA=Red, Q=Blue
  SA         Red        WA=Blue, NT=Green, Q=Blue, NSW=Green, V=Blue
  Q          Blue       NT=Green, SA=Red, NSW=Green
  NSW        Green      Q=Blue, SA=Red, V=Blue
  V          Blue       SA=Red, NSW=Green
  T          Red        —

── Constraint verification ───────────────────────────
  ✓ All constraints satisfied — no adjacent regions share a color.

── Search statistics ─────────────────────────────────
  Recursive calls : 7
  Backtracks      : 0
============================================================

── Constraint graph (unique edges) ──────────────────────
  NT ── WA
  SA ── WA
  NT ── SA
  NT ── Q
  Q  ── SA
  NSW ── SA
  SA ── V
  NSW ── Q
  NSW ── V

  Total constraints (edges): 9
  Total variables          : 7
  Domain size per variable : 3
```

### Final coloring

| Region | Color | Adjacent to |
|--------|-------|-------------|
| WA | 🔵 Blue | NT (Green), SA (Red) |
| NT | 🟢 Green | WA (Blue), SA (Red), Q (Blue) |
| SA | 🔴 Red | WA, NT, Q, NSW, V |
| Q | 🔵 Blue | NT (Green), SA (Red), NSW (Green) |
| NSW | 🟢 Green | Q (Blue), SA (Red), V (Blue) |
| V | 🔵 Blue | SA (Red), NSW (Green) |
| T | 🔴 Red | — (island, unconstrained) |

**0 backtracks** — the MRV + Forward Checking combo is so effective that the solver finds the solution on the very first attempt at each variable.

---

## Why No Backtracking Occurs

SA is chosen first (MRV picks it because it has the **most neighbors** = most constrained overall, degree heuristic). Once SA = Red is locked:

- Forward checking prunes Red from WA, NT, Q, NSW, V.
- NT now has only {Green, Blue} — MRV picks it next.
- Assigning NT = Green prunes Green from WA and Q.
- Q is now forced to Blue; NSW forced to Green; WA forced to Blue; V forced to Blue.

Every subsequent assignment is forced — there's only one option left. The algorithm never needs to backtrack.

---

## Key Concepts

| Concept | What it is |
|---------|------------|
| **Variable** | A region (WA, NT, SA, …) |
| **Domain** | Available colors for that region |
| **Constraint** | Adjacent regions must differ in color |
| **Arc consistency** | Neighboring domains are compatible |
| **MRV** | Pick the most constrained variable first |
| **Forward checking** | Prune domains after every assignment |
| **Backtracking** | Undo a bad assignment and try the next value |

---

## References

- Russell, S. & Norvig, P. — *Artificial Intelligence: A Modern Approach*, Chapter 6 (CSP)
- This problem is the canonical example used in that chapter.
