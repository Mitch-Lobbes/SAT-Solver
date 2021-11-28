from enum import Enum

from helper import negate_literal
from rules import Rules
import copy


class Algorithm(Enum):
    DPLL = 1
    JEROSLOW_WANG = 2
    DYNAMIC_VARIABLE_ORDERING = 3


class SATSolver:

    def __init__(self):
        self._true_literals: list[str] = []
        self._backtrack_count = 0
        self._split_count = 0
        pass

    def solve(self, rules: Rules, problem: list[str], algorithm: Algorithm) -> [bool, list[str], int, int]:
        # print("Solving new problem")
        self._reset()
        self._algorithm = algorithm
        self._initial_simplification(rules=rules, problem=problem)
        self._split_count += 1

        # Basic DPLL
        if algorithm == Algorithm.DPLL:
            initial_literal = rules.basic_DPLL()

        # ---JW---
        elif algorithm == Algorithm.JEROSLOW_WANG:
            rules.jerslow_wang_heuristic()
            initial_literal = rules.get_literal()

        # Dynamic Variable Ordering
        elif algorithm == Algorithm.DYNAMIC_VARIABLE_ORDERING:
            initial_literal = rules.dynamical_weight_variable_ordering()

        # ---MOM---
        # initial_literal = rules.moms_heuristic()

        neg_initial_literal = negate_literal(initial_literal)

        result = self._dpll(rules=copy.deepcopy(rules), literal=neg_initial_literal)
        if not result:
            result = self._dpll(rules=copy.deepcopy(rules), literal=initial_literal)

        truer_literals_set = set([lit for lit in self._true_literals if "-" not in lit])
        solution = list(truer_literals_set) + problem
        return result, solution, self._backtrack_count, self._split_count

    def _reset(self):
        self._backtrack_count = 0
        self._split_count = 0
        self._true_literals = []

    def _initial_simplification(self, rules: Rules, problem: list[str]):
        for literal in problem:
            rules.remove_or_shorten_clauses_containing_literal(literal=literal)

    def _dpll(self, rules: Rules, literal: str) -> bool:
        rules.remove_or_shorten_clauses_containing_literal(literal=literal)

        if not rules.contains_clauses():
            self._true_literals.append(literal)
            return True
        if rules.contains_empty_clauses():
            self._backtrack_count += 1
            return False

        # DO UNIT RULE
        unit_rule_literals = rules.unit_rule()

        for lit in unit_rule_literals:
            rules.remove_or_shorten_clauses_containing_literal(literal=lit)

            if lit in rules._literals:
                rules._literals.remove(lit)

            neg = negate_literal(lit)
            if neg in rules._literals:
                rules._literals.remove(neg)
            if '-' not in lit:
                self._true_literals.append(lit)

        if not rules.contains_clauses():
            self._true_literals.append(literal)
            return True
        if rules.contains_empty_clauses():
            self._backtrack_count += 1
            # print("CONFLICT")
            for lit in unit_rule_literals:
                if '-' not in lit:
                    self._true_literals.remove(lit)
            return False

        # Basic DPLL
        if self._algorithm == Algorithm.DPLL:
            next_literal = rules.basic_DPLL()

        # ---JW---
        elif self._algorithm == Algorithm.JEROSLOW_WANG:
            rules.jerslow_wang_heuristic()
            next_literal = rules.get_literal()

        # Dynamic Variable Ordering
        elif self._algorithm == Algorithm.DYNAMIC_VARIABLE_ORDERING:
            next_literal = rules.dynamical_weight_variable_ordering()

        self._split_count += 1

        # ---MOM---
        # next_literal = rules.moms_heuristic()

        neg_next_literal = negate_literal(literal=next_literal)

        if self._dpll(rules=copy.deepcopy(rules), literal=neg_next_literal):
            self._true_literals.append(neg_next_literal)
            return True
        temp_result = self._dpll(rules=copy.deepcopy(rules), literal=next_literal)
        if temp_result:
            self._true_literals.append(next_literal)
        else:
            self._backtrack_count += 1
            # Remove literals from solutions again
            for lit in unit_rule_literals:
                if '-' not in lit:
                    self._true_literals.remove(lit)
        return temp_result

# Variable State Independent Decaying Sum
# BCP = Boolean Constraint Propagation -> unit Rule
# CHB = conflict history-based branching heuristic
# UIP = Unique Implication Point

# clause class, save a list of literals that lead to the removal of individual literals
# -> Negate those literals and add as a clause
