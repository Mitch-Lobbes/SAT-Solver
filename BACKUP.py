import numpy as np
from collections import Counter


class Variables:

    def __init__(self, dict: dict):
        self._variable_dict = dict

    def set_value(self, key: int, value: int):
        self._variable_dict[key] = value

    def true_values(self):
        return [key for (key, value) in self._variable_dict.items() if value == 1]

    def false_values(self):
        return [key for (key, value) in self._variable_dict.items() if value == 0]

    def none_values(self):
        return [key for (key, value) in self._variable_dict.items() if value == None]

    def read_sudoku(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            number = line.split(" ")[0]
            self._variable_dict[number] = 1


SUDOKU_RULES_FILENAME = "sudoku-rules.txt"


class SATSolver:

    def __init__(self, sudoku_filename: str):
        # Variables
        self._variables = Variables
        self._rules = []
        self._pos_frequencies = Counter()
        self._log_dict = {}
        self._log_rules = {}
        self._tried = []

        self._initialize_dict()
        self._read_rules()

        self._variables.read_sudoku(filename=sudoku_filename)

        self.solve()

    def DLIS(self):

        self._pos_frequencies = {}

        for unit in self._variables.none_values():
            pos_counter = 0
            neg_counter = 0
            for rule in self._rules:
                if unit in rule:
                    pos_counter += 1
                if f"-{unit}" in rule:
                    neg_counter += 1

            pos_counter = pos_counter - neg_counter
            self._pos_frequencies[unit] = (pos_counter, neg_counter)

        highest_connections = max(self._pos_frequencies.values())
        highest_variable = list(self._pos_frequencies.keys())[list(self._pos_frequencies.values()).index(highest_connections)]

        if highest_variable not in self._tried:
            value = 0 if highest_connections[0] < highest_connections[1] else 1
            self._tried.append(highest_variable)
        else:
            value = 1 if highest_connections[0] < highest_connections[1] else 0


        print(highest_variable, value)
        return highest_variable, value


    def solve(self):

        print("Start Sudoku Solver")
        print("TRUE\tFALSE\tRULES")
        print(len(self._variables.true_values()),"\t\t",len(self._variables.false_values()),"\t\t",len(self._rules), '\n')

        run = 0

        while True:
            run += 1
            old_rules_ln = len(self._rules)

            self._log_dict[run] = self._variables._variable_dict.copy()
            self._log_rules[run] = self._rules.copy()

            self._remove_true_lines(self._variables.true_values())
            self._set_partner_value(self._variables.true_values(), 0)
            self._remove_true_literals(self._variables.false_values())

            if len(self._rules) == old_rules_ln:
                key, value = self.DLIS()
                self._variables.set_value(key=key,value=value)

            if not self._variables.none_values() and self._rules:
                print("Failed Attempt, Going to Backtrack")
                run = run - 1
                self._variables.variable_dict = self._log_dict[run].copy
                self._rules = self._log_rules[run].copy

            if not self._variables.none_values()  and not self._rules:
                print("Succes")
                break

            print(len(self._variables.true_values()), "\t\t", len(self._variables.false_values()), "\t",len(self._rules), '\n')

    def _remove_true_lines(self, true_values: list):
        for value in true_values:
            for rule in self._rules:
                if value in rule and not f"-{value}" in rule:
                    self._rules.remove(rule)

    def _remove_true_literals(self, false_values: list):
        # Go backwards
        for value in false_values:
            for rule in reversed(self._rules):
                if f"-{value}" in rule:
                    self._rules.remove(rule)

    def _set_partner_value(self, value_list: list, val: int):
        for rule in self._rules:
            for value in value_list:
                if f"-{value}" == rule.split(" ")[0]:
                    self._variables.set_value(
                        key=rule.split(" ")[1][1:],
                        value=val
                    )
                elif f"-{value}" == rule.split(" ")[1]:
                    self._variables.set_value(
                        key=rule.split(" ")[0][1:],
                        value=val
                    )

    def _initialize_dict(self):
        keylist = [str(x) for x in range(111, 1000)]

        keylist = list(filter(lambda value: "0" not in str(value), keylist))
        nones = [None] * len(keylist)
        self._variables = Variables(dict=dict(zip(keylist, nones)))

    def _read_rules(self):
        with open(SUDOKU_RULES_FILENAME) as f:
            self._rules = f.readlines()[1:]


SUDOKU_FILE = "sudoku-example.txt"
sat = SATSolver(SUDOKU_FILE)