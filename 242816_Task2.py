"""
CS344L - Artificial Intelligence Lab | Lab 5 - Constraint Satisfaction Problems
Task 2 - MRV and degree heuristics on the exam timetable  (roll 242816)

Same CSP as Task 1 (same variables, domain and clash constraint, same
is_consistent check). Only the order in which courses are picked changes:
plain backtracking takes the next course in the list, while the improved
search picks the most constrained course first (MRV + degree).
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
    # (Exactly the same check as in Task 1.)
    for other, other_slot in assignment.items():
        if other in CLASHES[course] and other_slot == slot:
            return False
    return True


def legal_slots(course, assignment):
    # The slots still possible for this course right now.
    return [s for s in SLOTS if is_consistent(course, s, assignment)]


def select_course(assignment):
    # MRV: pick the unscheduled course with the fewest legal slots left.
    # Tie-break with the degree rule: among those, pick the course that
    # clashes with the most courses that are still unscheduled.
    unscheduled = [c for c in COURSES if c not in assignment]
    best = None
    best_key = None
    for course in unscheduled:
        mrv = len(legal_slots(course, assignment))
        degree = sum(1 for other in CLASHES[course] if other in unscheduled)
        key = (mrv, -degree)  # fewer slots first, then higher degree
        if best_key is None or key < best_key:
            best = course
            best_key = key
    return best


def search(next_course):
    # Backtracking search where next_course(assignment) decides which
    # course to try next. Returns (assignment or None, pick order list).
    assignment = {}
    order = []  # (course, options left when it was picked)

    def backtrack():
        global tests, backtracks
        if len(assignment) == len(COURSES):
            return True
        course = next_course(assignment)
        options = legal_slots(course, assignment)
        order.append((course, options))
        for slot in SLOTS:
            tests += 1  # every slot tried counts, as in Task 1
            if is_consistent(course, slot, assignment):
                assignment[course] = slot
                if backtrack():
                    return True
                del assignment[course]  # undo the choice
                backtracks += 1
        order.pop()
        return False

    if backtrack():
        return assignment, order
    return None, order


def next_in_list(assignment):
    # Plain version: take the next course in the COURSES list.
    return COURSES[len(assignment)]


def main():
    # 1. Order chosen by the heuristics, with options left at each step.
    reset_counters()
    plan, order = search(select_course)
    print("Order chosen by MRV + degree:")
    for course, options in order:
        print(f"   pick {course:<10} options left: {options}")
    mrv_tests, mrv_backtracks = tests, backtracks
    print()

    # 2. Same problem with plain list order, for comparison.
    reset_counters()
    plan_plain, _ = search(next_in_list)
    plain_tests, plain_backtracks = tests, backtracks

    print("Comparison")
    print("   method                tests   backtracks")
    print(f"   plain backtracking    {plain_tests:<7} {plain_backtracks}")
    print(f"   MRV + degree          {mrv_tests:<7} {mrv_backtracks}")


if __name__ == "__main__":
    main()
