from helper import negate_literal
from rules import Rules
import copy


class SATSolver:

    def __init__(self):
        self._true_literals: list[str] = []
        pass

    def solve(self, rules: Rules, problem: list[str]) -> (bool, list[str]):
        print("Solving new problem")
        self._reset()
        self._initial_simplification(rules=rules, problem=problem)
        rules.jerslow_wang_heuristic()

        initial_literal = rules.get_literal()
        neg_initial_literal = negate_literal(initial_literal)

        result = self._dpll(rules=copy.deepcopy(rules), literal=neg_initial_literal)
        if not result:
            result = self._dpll(rules=copy.deepcopy(rules), literal=initial_literal)

        truer_literals_set = set([lit for lit in self._true_literals if "-" not in lit])
        solution = list(truer_literals_set) + problem
        return result, solution

    def _reset(self):
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
                pass
                self._true_literals.append(lit)

        if not rules.contains_clauses():
            self._true_literals.append(literal)
            return True
        if rules.contains_empty_clauses():
            for lit in unit_rule_literals:
                if '-' not in lit:
                    self._true_literals.remove(lit)
            return False

        rules.jerslow_wang_heuristic()

        next_literal = rules.get_literal()
        neg_next_literal = negate_literal(literal=next_literal)

        if self._dpll(rules=copy.deepcopy(rules), literal=neg_next_literal):
            self._true_literals.append(neg_next_literal)
            return True
        temp_result = self._dpll(rules=copy.deepcopy(rules), literal=next_literal)
        if temp_result:
            self._true_literals.append(next_literal)
        else:
            # Remove literals from solutions again
            for lit in unit_rule_literals:
                if '-' not in lit:
                    self._true_literals.remove(lit)
            pass
        return temp_result
