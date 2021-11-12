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

        while True:

            environment = Environment(
                variables=variables,
                rules=rules
            ) if not backtrack else self._environments[-backtrack_value]

            self._environments.append(environment)
            signal, (variables, rules) = environment.run()

            if not signal:
                for i in range (1, len(self._environments) + 1):
                    if self._environments[-i]._flip_last_variable():
                        backtrack = True
                        backtrack_value = i
                        break
            if not len(self._variables.none_values()) and not len(environment._initial_rules):
                print('Everything is fine')
                break


SUDOKU_FILE = "sudoku-example.txt"
sat = SATSolver(SUDOKU_FILE)
sat.run()
