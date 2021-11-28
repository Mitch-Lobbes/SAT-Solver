import time
import csv

from rules import Rules
from sat_solver import SATSolver, Algorithm

SUDOKU_RULES_FILEPATH = "rules/sudoku-rules-9x9.txt"


def read_sudoku(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]


def get_sudoku_and_rules_based_on_name(sudoku_filepath: str) -> (list[str], Rules):
    sudoku = read_sudoku(filepath=sudoku_filepath)
    rules = Rules(filepath=SUDOKU_RULES_FILEPATH)
    return sudoku, rules

STAT_HEADER = ['amount_vars', 'sudoku_idx', 'solving_time', 'avg_backtracks', 'avg_splits']

counter = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0,
    24: 0,
    25: 0,
    26: 0,
    27: 0,
    28: 0,
    29: 0
}

class StatCreator:

    def __init__(self):
        self._sat_solver = SATSolver()

    def run(self, sudoku_filepathes: list[str], algorithm: Algorithm, run: int = 10 ):
        f = open(f'results/new{algorithm}.csv', 'w', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(STAT_HEADER)

        for sudoku_filepath in sudoku_filepathes:
            print(f"Running: {sudoku_filepath}")
            num_vars = sum(1 for line in open(sudoku_filepath) if line.strip())
            sudoku, rules = get_sudoku_and_rules_based_on_name(sudoku_filepath=sudoku_filepath)
            avg_time, avg_backtrack, avg_split = self._average_time_on_n_runs(sudoku=sudoku, rules=rules, amount_runs=run, algorithm=algorithm)
            #print(f"{sudoku_index}: avg_time={avg_time}, avg_backtrack={avg_backtrack}")
            sudoku_index = counter[num_vars]
            counter[num_vars] += 1
            writer.writerow([num_vars, sudoku_index, avg_time, avg_backtrack, avg_split])

    def _average_time_on_n_runs(self, sudoku: list[str], rules: Rules, amount_runs: int, algorithm: Algorithm) -> (float, float):
        time_sum = 0
        backtrack_sum = 0
        split_sum = 0
        for _ in range(amount_runs):
            #print("New Run")
            start = time.time()
            satisfiable, solutions, backtrack_count, split_count = self._sat_solver.solve(rules=rules, problem=sudoku, algorithm=algorithm)
            backtrack_sum += backtrack_count
            split_sum += split_count
            end = time.time()
            time_sum += end - start
        time_avg = time_sum / amount_runs
        backtrack_avg = backtrack_sum / amount_runs
        avg_split = split_sum / amount_runs
        return time_avg, backtrack_avg, avg_split
