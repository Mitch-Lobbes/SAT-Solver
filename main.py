import numpy as np
from collections import Counter


class Variables:

    def __init__(self, dict: dict):
        self._variables_dict = dict

    def set_value(self, key: int, value: int):
        self._variables_dict[key] = value

    def true_values(self):
        return [key for (key, value) in self._variables_dict.items() if value == 1]

    def false_values(self):
        return [key for (key, value) in self._variables_dict.items() if value == 0]

    def none_values(self):
        return [key for (key, value) in self._variables_dict.items() if value == None]

    def read_sudoku(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            number = line.split(" ")[0]
            self._variables_dict[number] = 1


class Clause:
    """
    Clause containing only "or" conjunctions
    """

    def __init__(self, positive_variables: list[str], negative_variables: list[str]):
        self._positive_variables = positive_variables
        self._negative_variables = negative_variables

    def contains_variable(self, variable: str) -> bool:
        return variable in self._negative_variables or variable in self._positive_variables

    def positive_variables(self) -> list[str]:
        return self._positive_variables

    def negative_variables(self) -> list[str]:
        return self._negative_variables


class Rules:

    def __init__(self, filepath: str):
        self._rules = []
        self._clauses = []
        self._variables_set = {}
        self._variable_occurrences = []
        self._read_rules(filepath=filepath)

    def _read_rules(self, filepath: str):
        with open(filepath) as f:
            self._rules = f.readlines()[1:]

    def _convert_rules_to_clauses(self):
        for rule in self._rules:
            variables = rule.split()
            negative_vars = [var for var in variables if '-' in var]
            positive_vars = [var[1:] for var in variables if '-' not in var and var != "0"]
            self._variables_set.update(negative_vars)
            self._variables_set.update(positive_vars)

            clause = Clause(
                negative_variables=negative_vars,
                positive_variables=positive_vars
            )
            self._clauses.append(clause)

    def _count_variable_occurrences(self):
        # Initialize all to zero
        for var in self._variables_set:
            self._variable_occurrences[var] = (0, 0)

        for clause in self._clauses:
            positive_variables = clause.positive_variables()
            negative_variables = clause.negative_variables()
            for var in positive_variables:
                self._variable_occurrences[var][0] += 1
            for var in negative_variables:
                self._variable_occurrences[var][1] += 1

    def simplication(self):
        pass

    def simplication_tautology(self):
        pass

    def simplication_pure_literal(self):
        pass

    def simplication_unit_clause(self):
        pass


class Environment:

    def __init__(self, variables: Variables, rules: Rules):
        self._variables = variables
        self._rules = rules

    def _remove_true_lines(self):
        """ Remove clauses from rules, based on variable values
        """
        true_values = self._variables.true_values()
        for value in true_values:
            for rule in self._rules:
                if value in rule and not f"-{value}" in rule:
                    self._rules.remove(rule)


SUDOKU_RULES_FILENAME = "sudoku-rules.txt"


class SATSolver:

    def __init__(self, sudoku_filename: str):
        # Variables
        self._variables = Variables
        self._rules = []
        self._pos_frequencies = Counter()
        self._neg_frequencies = Counter()
        self._log_dict = {}
        self._log_rules = {}
        self.tried = []
        self.last_updated_nr = None

        self._initialize_dict()
        self._read_rules()

        self._variables.read_sudoku(filename=sudoku_filename)

        self.solve()

    def DLIS(self):

        # Save current dictionary and rules based on run
        for sentence in self._rules:
            self._neg_frequencies.update(
                word.strip('.,?!"\'').lower() for word in sentence.split() if word != '0' and '-' in word)
            self._pos_frequencies.update(
                word.strip('.,?!"\'').lower() for word in sentence.split() if word != '0' and '-' not in word)

        highest_neg_nr = self._neg_frequencies.most_common(1)[0][0]
        highest_neg_fre = self._neg_frequencies.most_common(1)[0][1]
        highest_pos_nr = highest_neg_nr[1:]
        highest_pos_fre = self._pos_frequencies[highest_pos_nr]

        if highest_pos_nr not in self.tried:
            value = 1 if highest_pos_fre > highest_neg_fre else 0
        else:
            value = 0 if highest_pos_fre > highest_neg_fre else 1
            del self._pos_frequencies[highest_pos_nr]
            del self._neg_frequencies[highest_neg_nr]

        print("Highest Connected Literal", highest_pos_nr, "Should be set to", value)

        self.tried.append(highest_pos_nr)
        self.last_updated_nr = highest_pos_nr

        return highest_pos_nr, value

    def solve(self):

        print("Start Sudoku Solver")
        print("TRUE\tFALSE\tRULES")
        print(len(self._variables.true_values()), "\t\t", len(self._variables.false_values()), "\t\t", len(self._rules),
              '\n')

        while True:

            old_rules_ln = len(self._rules)

            self._remove_true_lines(self._variables.true_values())
            self._set_partner_value(self._variables.true_values(), 0)
            self._remove_true_literals(self._variables.false_values())

            if len(self._rules) == old_rules_ln:
                key, value = self.DLIS()
                self._variables.set_value(key=key, value=value)

            print(len(self._variables.true_values()), "\t\t", len(self._variables.false_values()), "\t",
                  len(self._rules), '\n')

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
