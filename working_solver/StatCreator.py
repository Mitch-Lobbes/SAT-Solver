import time

from rules import Rules
from sat_solver import SATSolver

SUDOKU_RULES_FILEPATH = "rules/sudoku-rules-9x9.txt"


def read_sudoku(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]


def get_sudoku_and_rules_based_on_index(sudoku_index: int) -> (list[str], Rules):
    sudoku_filepath = f"example_sudokus/sudoku-example-{sudoku_index}"
    sudoku = read_sudoku(filepath=sudoku_filepath)
    rules = Rules(filepath=SUDOKU_RULES_FILEPATH)
    return sudoku, rules


class StatCreator:

    def __init__(self):
        self._sat_solver = SATSolver()

    def run(self, sudokus_indexes: list[int], run: int = 10):

        for sudoku_index in sudokus_indexes:
            sudoku, rules = get_sudoku_and_rules_based_on_index(sudoku_index=sudoku_index)
            avg_time = self._average_time_on_n_runs(sudoku=sudoku, rules=rules, amount_runs=run)
            print(f"Average time on sudoku {sudoku_index}: {avg_time}")

        pass

    def _average_time_on_n_runs(self, sudoku: list[str], rules: Rules, amount_runs: int) -> float:
        time_sum = 0
        for _ in range(amount_runs):
            start = time.time()
            self._sat_solver.solve(rules=rules, problem=sudoku)
            end = time.time()
            time_sum += end - start
        time_avg = time_sum / amount_runs
        return time_avg
