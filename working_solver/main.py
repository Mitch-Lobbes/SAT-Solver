import copy
from rules import Rules

# 9x9
"sudoku-rules.txt"
"sudoku-example.txt"

SUDOKU_RULES_FILEPATH = "sudoku-rules-4x4.txt"
SUDOKU_EXAMPLE_FILEPATH = "sudoku-example4.txt"

def read_example(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        return [clause[:-3] for clause in lines]

idx = 0
true_literals = []

def dpll_2(rules: Rules, literal: str) -> bool:
    global idx
    global true_literals
    print(f"-- New DPLL idx: {idx}")
    idx = idx + 1
    # Remove clauses from α containing literal
    # Shorten clauses from α containing -literal
    rules.remove_or_shorten_clauses_containing_literal(literal=literal)

    if not rules.contains_clauses():
        true_literals.append(literal)
        return True
    if rules.contains_empty_clauses():
        print("-------EMPTY CLAUSES ------------")
        #true_literals = true_literals[:-len(unit_list)]
        return False

    # DO UNIT RULE
    rules.unit_rule()

    #for uliterals in unit_rule_literals:
        #neg_uliteral = f"-{uliterals}" if not "-" in uliterals else uliterals[1:]
        #if neg_uliteral in unit_rule_literals or neg_uliteral in true_literals:
        #    return False
        #true_literals.append(uliterals.replace("-", ""))


    # next_literal = rules.pick_random_literal()
    rules.jerslow_wang_heuristic()
    next_literal = rules.get_literal()

    neg_next_literal = f"-{next_literal}" if not "-" in next_literal else next_literal[1:]
    if dpll_2(rules=copy.deepcopy(rules), literal=neg_next_literal):
        true_literals.append(literal)
        return True
    temp_result = dpll_2(rules=copy.deepcopy(rules), literal=next_literal)
    if temp_result:
        true_literals.append(literal)
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
    result = dpll_2(rules=rules, literal=initial_literal)

true_true_literals = set([lit for lit in true_literals if "-" not in lit])
print(true_true_literals)
print(len(true_true_literals))
print(result)
