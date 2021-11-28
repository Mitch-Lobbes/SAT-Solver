import copy
from rules import Rules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from helper import negate_literal, plot_sudoku

# 9x9
# "sudoku-rules.txt"
# "sudoku-example.txt"

#SUDOKU_RULES_FILEPATH = "sudoku-rules-4x4.txt"
#SUDOKU_EXAMPLE_FILEPATH = "sudoku-example4.txt"
from sat_solver import SATSolver

SUDOKU_RULES_FILEPATH = "rules/sudoku-rules-9x9.txt"
SUDOKU_EXAMPLE_FILEPATH = "example_sudokus/sudoku-example-1.txt"


def read_example(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]



sudoku = read_example(SUDOKU_EXAMPLE_FILEPATH)
rules = Rules(filepath=SUDOKU_RULES_FILEPATH)

sat_solver = SATSolver()

result, solution = sat_solver.solve(rules = rules, problem=sudoku)

#print(solution)
#print(len(solution))
print(result)

s = int(max(solution)[0])
size = (s, s)
matrix = np.zeros(size)

for sol in solution:
    row = int(sol[0]) - 1
    col = int(sol[1]) - 1
    num = int(sol[2])
    matrix[row][col] = num

matrix = matrix.astype(int)
print(matrix)

#plot_sudoku(matrix)
