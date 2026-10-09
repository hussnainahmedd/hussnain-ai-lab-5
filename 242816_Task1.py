"""
CS344L - Artificial Intelligence Lab | Lab 5 - Constraint Satisfaction Problems
Task 1 - Exam timetable as a CSP  (roll 242816)

CSP model (in my own words):
  Variables : the six courses that each need an exam slot.
  Domain    : the three days {Monday, Tuesday, Wednesday} - the same for
              every course.
  Constraint: two courses that share students (a clash) may not have their
              exams on the same day.
"""

COURSES = ["AI", "Database", "Networks", "OS", "Compiler", "Graphics"]

SLOTS = ["Monday", "Tuesday", "Wednesday"]

CLASHES = {
    "AI":       ["Database", "Networks", "OS"],
    "Database": ["AI", "Networks", "Graphics"],
    "Networks": ["AI", "Database", "OS", "Graphics"],
    "OS":       ["AI", "Networks", "Compiler"],
    "Compiler": ["OS", "Graphics"],
    "Graphics": ["Database", "Networks", "Compiler"],
}

tests = 0        # how many slot assignments were tried
backtracks = 0   # how many times a choice had to be undone


def reset_counters():
    # Set both counters back to zero before a new search.
    global tests, backtracks
    tests = 0
    backtracks = 0


def is_consistent(course, slot, assignment):
    # True only if no clashing course already holds that slot.
    for other, other_slot in assignment.items():
        if other in CLASHES[course] and other_slot == slot:
            return False
    return True


def backtracking_search(courses, slots):
    # Assign a slot to every course in list order. When no slot fits the
    # current course, undo the last choice (backtrack) and try its next slot.
    assignment = {}

    def backtrack(i):
        global tests, backtracks
        if i == len(courses):
            return True
        course = courses[i]
        for slot in slots:
            tests += 1
            if is_consistent(course, slot, assignment):
                assignment[course] = slot
                if backtrack(i + 1):
                    return True
                del assignment[course]  # undo the choice
                backtracks += 1
        return False

    if backtrack(0):
        return assignment
    return None


def print_timetable(plan):
    # Print one course per line, aligned in two columns.
    for course in COURSES:
        print(f"   {course:<10} {plan[course]}")


def main():
    # Solve once with three slots, then again with only two slots.
    print("Exam timetable (3 slots)")
    reset_counters()
    plan = backtracking_search(COURSES, SLOTS)
    print_timetable(plan)
    print(f"   tests: {tests}, backtracks: {backtracks}")
    print()

    print("With only 2 slots: ", end="")
    reset_counters()
    plan2 = backtracking_search(COURSES, SLOTS[:2])
    if plan2 is None:
        print("no valid timetable exists")
    else:
        print()
        print_timetable(plan2)
    print(f"   tests: {tests}, backtracks: {backtracks}")


if __name__ == "__main__":
    main()
