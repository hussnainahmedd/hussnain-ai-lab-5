"""
CS344L - Artificial Intelligence Lab | Lab 5 - Constraint Satisfaction Problems
Task 3 - 8-Queens with your own roll number  (roll 242816)

CSP model (in my own words):
  Variables : the eight columns of the board (one queen per column).
  Domain    : the eight rows {0..7} - the same for every column.
  Constraints: (1) no two queens share a row;
               (2) no two queens share a diagonal - two queens share a
               diagonal exactly when their row difference equals their
               column difference.
               Plus the extra rule: the queen in column 0 is fixed to
               row (roll number mod 8).

Run:  python 242816_Task3.py            -> uses your own row (roll mod 8)
      python 242816_Task3.py 4          -> first queen forced into row 4
"""

import sys

N = 8
ROLL_NUMBER = 242816
START_ROW = ROLL_NUMBER % N  # 242816 % 8 = 0


def is_safe(column, row, assignment):
    # True only if a queen at (column, row) breaks neither the row rule
    # nor the diagonal rule against the queens already placed.
    for c, r in assignment.items():
        if r == row:
            return False
        if abs(r - row) == abs(c - column):
            return False
    return True


def solve(start_row):
    # Backtracking search with column 0 already fixed to start_row.
    # Tries rows 0..7 in each next column, undoing the last placement
    # (backtrack) when no row fits. Returns (assignment, placements, backtracks).
    assignment = {0: start_row}
    placements = 0   # rows tried
    backtracks = 0   # placements undone

    def backtrack(column):
        nonlocal placements, backtracks
        if column == N:
            return True
        for row in range(N):
            placements += 1
            if is_safe(column, row, assignment):
                assignment[column] = row
                if backtrack(column + 1):
                    return True
                del assignment[column]  # undo the placement
                backtracks += 1
        return False

    if backtrack(1):
        return assignment, placements, backtracks
    return None, placements, backtracks


def print_board(assignment):
    # Print the board using Q for queens and . for empty squares.
    print("     " + " ".join(str(c) for c in range(N)))
    for row in range(N):
        line = []
        for col in range(N):
            line.append("Q" if assignment.get(col) == row else ".")
        print(f"   {row} " + " ".join(line))
    print()


def verify(assignment):
    # Check every pair of queens; the board is safe only if no pair
    # shares a row or a diagonal.
    cols = sorted(assignment)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            c1, c2 = cols[i], cols[j]
            r1, r2 = assignment[c1], assignment[c2]
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def main():
    # Optional command-line row overrides the roll-number row (for Q6).
    start_row = int(sys.argv[1]) if len(sys.argv) > 1 else START_ROW

    print(f"Roll number: {ROLL_NUMBER}, "
          f"so column 0 queen is in row {start_row}")
    print()
    assignment, placements, backtracks = solve(start_row)
    print_board(assignment)
    print(f"   placements tried: {placements}")
    print(f"   backtracks      : {backtracks}")
    print(f"   verified safe   : {verify(assignment)}")


if __name__ == "__main__":
    main()
