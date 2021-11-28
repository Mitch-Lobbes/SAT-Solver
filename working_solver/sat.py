import sys
from enum import Enum

from rules import Rules
from sat_solver import SATSolver, Algorithm


def read_example(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]


SUDOKU_RULES_FILEPATH = "rules/sudoku-rules-9x9.txt"
SUDOKU_EXAMPLE_FILEPATH = "example_sudokus/sudoku-example-1"


def main() -> None:
    # General input checks
    if not check_arguments():
        usage()
        return

    algorithm = Algorithm(int(sys.argv[1][2]))
    inputfile = sys.argv[2]

    sudoku = read_example(SUDOKU_EXAMPLE_FILEPATH)
    rules = Rules(filepath=SUDOKU_RULES_FILEPATH)

    sat_solver = SATSolver()

    result, solution, amount_backtracks = sat_solver.solve(rules=rules, problem=sudoku, algorithm=algorithm)

    print(result)
    print(len(solution))
    print(amount_backtracks)


def check_arguments() -> bool:
    """Check if command line arguments are correct"""
    if len(sys.argv) != 3:
        return False
    if len(sys.argv[1]) != 3:
        return False
    if not sys.argv[1].startswith("-S"):
        return False
    if sys.argv[1][2] not in ["1", "2", "3"]:
        return False
    return True


def usage() -> None:
    print("""Usage:
    SAT -S<strategy> inputfile
    -strategy: Strategy to use in the SAT solver.
               1 = Basic DPLL
               2 = One sided Jeroslow-Wang
               3 = Dynamic variable ordering
    inputfile: Concatenation of all required input clauses
Example: SAT -S2 example_sudoku.txt""")


if __name__ == "__main__":
    main()
