import copy

from helper import negate_literal
from rules import Rules
import numpy as np

# 9x9
# "sudoku-rules.txt"
# "sudoku-example.txt"

#SUDOKU_RULES_FILEPATH = "sudoku-rules-4x4.txt"
#SUDOKU_EXAMPLE_FILEPATH = "sudoku-example4.txt"

SUDOKU_RULES_FILEPATH = "sudoku-rules.txt"
SUDOKU_EXAMPLE_FILEPATH = "sudoku-example.txt"


def read_example(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]


idx = 0
true_literals = []
literals_added = []


def dpll_2(rules: Rules, literal: str) -> bool:
    global idx
    global true_literals
    #print(f"-- New DPLL idx: {idx}")
    #idx = idx + 1

    rules.remove_or_shorten_clauses_containing_literal(literal=literal)

    if not rules.contains_clauses():
        true_literals.append(literal)
        return True
    if rules.contains_empty_clauses():
        return False

    # DO UNIT RULE
    unit_rule_literals = rules.unit_rule()
    for lit in unit_rule_literals:
        rules.remove_or_shorten_clauses_containing_literal(literal=lit)

        if lit in rules._literals:
            rules._literals.remove(lit)

        neg = literal[1:] if '-' in literal else f'-{literal}'
        if neg in rules._literals:
            rules._literals.remove(neg)
        if '-' not in lit:
            pass
            true_literals.append(lit)

    if not rules.contains_clauses():
        true_literals.append(literal)
        #print("SULUTION FOUND")
        return True
    if rules.contains_empty_clauses():
        #print("RETURN FALSE IN EMPTY CLAUSE")
        # TODO: REMOVE fRoM TRUE unit
        for lit in unit_rule_literals:
            if '-' not in lit:
                true_literals.remove(lit)
        return False

    rules.jerslow_wang_heuristic()

    next_literal = rules.get_literal()
    neg_next_literal = negate_literal(literal=next_literal)

    if dpll_2(rules=copy.deepcopy(rules), literal=neg_next_literal):
        true_literals.append(neg_next_literal)
        return True
    temp_result = dpll_2(rules=copy.deepcopy(rules), literal=next_literal)
    if temp_result:
        true_literals.append(next_literal)
    else:
        # Remove literals from solutions again
        for lit in unit_rule_literals:
            if '-' not in lit:
                true_literals.remove(lit)
        pass
    return temp_result


sudoku = read_example(SUDOKU_EXAMPLE_FILEPATH)
rules = Rules(filepath=SUDOKU_RULES_FILEPATH)

for literal in sudoku:
    rules.remove_or_shorten_clauses_containing_literal(literal=literal)

rules.jerslow_wang_heuristic()

initial_literal = rules.get_literal()
neg_initial_literal = f"-{initial_literal}" if not "-" in initial_literal else initial_literal[1:]
result = dpll_2(rules=copy.deepcopy(rules), literal=neg_initial_literal)
if not result:
    result = dpll_2(rules=copy.deepcopy(rules), literal=initial_literal)

true_true_literals = set([lit for lit in true_literals if "-" not in lit])
three_three_literals = set([lit for lit in true_literals if "-" not in lit and lit.startswith("33")])
solution = list(true_true_literals) + sudoku

#print(solution)
#print(len(solution))
print(result)
"""
s = int(max(solution)[0])
size = (s, s)
matrix = np.zeros(size)

for sol in solution:
    row = int(sol[0]) - 1
    col = int(sol[1]) - 1
    num = int(sol[2])
    matrix[row][col] = num

print(matrix)
"""
