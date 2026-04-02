# Sudoku Puzzle Solver using CSP

This project is a Sudoku Puzzle Solver implemented using the Constraint Satisfaction Problem (CSP) approach. In this program, each of the 81 cells in the Sudoku board is treated as a variable, the possible values for each cell form its domain, and the rules of Sudoku act as constraints. The solver uses a combination of Backtracking Search, Forward Checking, Minimum Remaining Values (MRV), and AC-3 Arc Consistency to solve the puzzle efficiently. Instead of blindly trying values, the program reduces the search space by removing invalid possibilities early, which makes solving faster and more intelligent. The code also displays the puzzle in a formatted 9×9 board, shows the solved result, and prints the time taken to solve each puzzle.

## Requirements
- Python 3.x
- No external libraries are required
- Only standard Python modules are used (`copy` and `time`)

## How It Works
The Sudoku puzzle is stored as a list of 81 integers where `0` represents an empty cell. The solver first creates domains for all cells. If a cell already has a value, its domain contains only that value. If a cell is empty, its domain starts with all digits from 1 to 9. The program then applies AC-3 Arc Consistency to remove inconsistent values from domains before starting the main search. After that, Backtracking Search is used to assign values to unfilled cells. The MRV heuristic is used to choose the next unassigned cell with the smallest remaining domain, which helps the solver focus on the most constrained cell first. Once a value is assigned, Forward Checking removes that value from all related peer cells in the same row, column, and 3×3 box. If this creates a contradiction, the solver undoes the changes and backtracks. This continues until either the puzzle is completely solved or no valid solution exists.

## File Name
Save the code in a Python file such as:
`sudoku_solver.py`

## How to Run
1. Save the program in a file named `sudoku_solver.py`
2. Open a terminal or command prompt in the same folder
3. Run the program using:
```bash
python sudoku_solver.py or python3 sudoku_solver.py

```
```
═══════════════════════════════════
  Sudoku Solver — CSP
  Backtracking + FC + MRV + AC-3
═══════════════════════════════════

═══════════════════════════════════
  Puzzle: Easy
═══════════════════════════════════

  Initial Board:
┌───────┬───────┬───────┐
│ 5 3 ·│ · 7 ·│ · · · │
│ 6 · ·│ 1 9 5│ · · · │
│ · 9 8│ · · ·│ · 6 · │
├───────┼───────┼───────┤
│ 8 · ·│ · 6 ·│ · · 3 │
│ 4 · ·│ 8 · 3│ · · 1 │
│ 7 · ·│ · 2 ·│ · · 6 │
├───────┼───────┼───────┤
│ · 6 ·│ · · ·│ 2 8 · │
│ · · ·│ 4 1 9│ · · 5 │
│ · · ·│ · 8 ·│ · 7 9 │
└───────┴───────┴───────┘

  Solved Board:
┌───────┬───────┬───────┐
│ 5 3 4│ 6 7 8│ 9 1 2 │
│ 6 7 2│ 1 9 5│ 3 4 8 │
│ 1 9 8│ 3 4 2│ 5 6 7 │
├───────┼───────┼───────┤
│ 8 5 9│ 7 6 1│ 4 2 3 │
│ 4 2 6│ 8 5 3│ 7 9 1 │
│ 7 1 3│ 9 2 4│ 8 5 6 │
├───────┼───────┼───────┤
│ 9 6 1│ 5 3 7│ 2 8 4 │
│ 2 8 7│ 4 1 9│ 6 3 5 │
│ 3 4 5│ 2 8 6│ 1 7 9 │
└───────┴───────┴───────┘

  ✓ Solved in 3.4 ms
```
