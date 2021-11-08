import numpy as np
from pprint import pprint


# /Users/robinbux/anaconda3/envs/KR/bin/python solver.py

class Variables:

    def __init__(self, dict: dict):
        self._variable_dict = dict

    def set_value(self, key: int, value: int):
        self._variable_dict[key] = value

    def true_values(self):
        return [key for (key, value) in self._variable_dict.items() if value == 1]

    def false_values(self):
        return [key for (key, value) in self._variable_dict.items() if value == 0]

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
        self._variables: Variables
        self._rules = []

        self._initialize_dict()
        self._read_rules()

        self._variables.read_sudoku(filename=sudoku_filename)

        print("TRUE = " ,len(self._variables.true_values()))
        print("FALSE = ", len(self._variables. false_values()))
        print("LENGTH RULES = ", len(self._rules))

        self.solve()

        print("TRUE = ", len(self._variables.true_values()))
        print("FALSE = ", len(self._variables.false_values()))
        print("LENGTH RUlES = ", len(self._rules))

    def solve(self):
        while(True):
            old_rules_ln = len(self._rules)
            self._remove_true_lines(self._variables.true_values())
            self._set_partner_value(self._variables.true_values(), 0)
            self._remove_true_literals(self._variables.false_values())
            if len(self._rules) == old_rules_ln:
                break


    def _remove_true_lines(self, true_values: list):
        for value in true_values:
            for rule in self._rules:
                if value in rule and not f"-{value}" in rule:
                    self._rules.remove(rule)

    def _remove_true_literals(self, false_values: list):
        # Go backwards
        for value in false_values:
            for i in range(len(self._rules) - 1, -1, -1):
                if f"-{value}" in self._rules[i]:
                    del self._rules[i]

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
            self._rules = f.readlines()


SUDOKU_FILE = "sudoku-example.txt"
sat = SATSolver(SUDOKU_FILE)
