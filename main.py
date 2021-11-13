from collections import Counter

from Environment import Environment
from Rules import Rules
from Variables import Variables

SUDOKU_RULES_FILEPATH = "sudoku-rules.txt"


class SATSolver:

    def __init__(self, sudoku_filename: str):
        # Variables
        self._variables = Variables()
        self._environments = []
        self._variables.read_sudoku(filename=sudoku_filename)

    def run(self):

        variables = self._variables
        rules = Rules(filepath=SUDOKU_RULES_FILEPATH)

        backtrack = False
        backtrack_value = 0
        id = 0
        while True:

            environment = Environment(
                variables=variables,
                rules=rules,
                id=id
            ) if not backtrack else self._environments[-backtrack_value]
            if not backtrack:
                id = id + 1

            if not backtrack:
                print("--------------------------------------")
                print('New Environment Created')
                self._environments.append(environment)
            signal, (variables, rules) = environment.run()
            print(len(self._variables.true_values()), len(self._variables.false_values()), rules.get_length())

            print(f"Signal: {signal}")
            if not signal:
                print("NOT SIGNAL")
                for i in range (2, len(self._environments) + 1):
                    if self._environments[-i].flip_last_variable():
                        backtrack = True
                        backtrack_value = i
                        print('Backtracking....')
                        break
            if not len(self._variables.none_values()) and not environment._initial_rules.get_length():
                print('Everything is fine')
                break


SUDOKU_FILE = "sudoku-example.txt"
sat = SATSolver(SUDOKU_FILE)
sat.run()
