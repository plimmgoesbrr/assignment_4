# Telangana District Map Coloring using CSP (Constraint Satisfaction Problem)

## Description

This project solves the **Map Coloring Problem** for the **33 districts of Telangana** using a Constraint Satisfaction Problem (CSP) approach. The goal is to assign a color to each district such that no two neighboring (border-sharing) districts have the same color — using only **4 colors**.

### Algorithm

The solver uses **Backtracking Search** enhanced with two optimizations:

1. **Forward Checking** — After assigning a color to a district, the algorithm immediately removes that color from the domains (available colors) of all unassigned neighboring districts. If any neighbor's domain becomes empty, the branch is pruned early, avoiding unnecessary recursion.

2. **MRV (Minimum Remaining Values) Heuristic** — At each step, the algorithm selects the unassigned district with the fewest remaining legal colors. This reduces the search space by tackling the most constrained variables first.

### CSP Formulation

| Element | Definition |
|---|---|
| Variables | 33 districts of Telangana |
| Domain | { Red, Green, Blue, Yellow } |
| Constraint | No two adjacent (border-sharing) districts may share the same color |

### Output

- A **color-coded table** in the terminal listing each district and its assigned color
- A **PNG graph image** (`telangana_map_coloring.png`) showing districts as nodes with edges between neighbors, each node colored according to the solution
- A **validity check** confirming no two adjacent districts share the same color

---

## Requirements

- Python 3.8 or higher
- matplotlib

Install the required library with:
```bash
pip install matplotlib
```

---

## How to Run

1. Make sure Python is installed. Download from [https://python.org](https://python.org) if needed.  
   *(On Windows, check "Add Python to PATH" during installation.)*

2. Install the dependency:
```bash
   pip install matplotlib
```

3. Run the script:
```bash
   python telangana_map_coloring.py
```

4. The terminal will display the coloring table and a confirmation that no adjacent districts share a color. A graph image will also be saved as `telangana_map_coloring.png` in the same folder.

---

## Files

| File | Description |
|---|---|
| `telangana_map_coloring.py` | Main Python script containing the CSP solver and visualisation |
| `telangana_map_coloring.png` | Output graph image generated after running the script |
| `README.md` | This file |

---

## Sample Output
```
Solving CSP Map Coloring for 33 districts of Telangana …

═══════════════════════════════════════════════════════
  Map Coloring — 33 Districts of Telangana (CSP)
═══════════════════════════════════════════════════════

  District                            Color
  --------------------------------------------------
  Adilabad                            Red
  Kumuram Bheem                       Green
  Mancherial                          Blue
  Nirmal                              Green
  Nizamabad                           Blue
  ...

✓ Valid coloring — no adjacent districts share a color!
```
