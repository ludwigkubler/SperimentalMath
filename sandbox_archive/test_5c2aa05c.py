# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_random_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def evaluate_formula(formula, assignment):
    return all(any(assignment[abs(lit) - 1] == l for l in clause) for clause in formula)

def fourier_coefficient(formula, S):
    n = len(S)
    sum_val = 0
    for i in range(2**n):
        assignment = [None] * (max(S) + 1)
        for j in range(n):
            assignment[S[j]] = ((i >> j) & 1) * 2 - 1
        sum_val += evaluate_formula(formula, assignment)
    return sum_val / 2**n

def resolution_length(formula):
    def dpll_with_learning(clauses, assignment, unit_clause_stack, learned_clauses):
        if not clauses:
            return True
        if len(unit_clause_stack) > 0:
            literal = unit_clause_stack.pop()
            assignment[abs(literal) - 1] = literal // abs(literal)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            learned_clauses.append([literal])
            return dpll_with_learning(new_clauses, assignment, unit_clause_stack, learned_clauses)
        pure_literal = find_pure_literal(clauses, assignment)
        if pure_literal is not None:
            assignment[abs(pure_literal) - 1] = pure_literal // abs(pure_literal)
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            learned_clauses.append([pure_literal])
            return dpll_with_learning(new_clauses, assignment, unit_clause_stack, learned_clauses)
        pure_symbol = find_pure_symbol(clauses, assignment)
        if pure_symbol is not None:
            new_clauses = [c for c in clauses if pure_symbol not in c and -pure_symbol not in c]
            learned_clauses.append([pure_symbol])
            return dpll_with_learning(new_clauses, assignment, unit_clause_stack, learned_clauses)
        literal = find_unit_clause(clauses, assignment)
        if literal is not None:
            unit_clause_stack.append(literal)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            learned_clauses.append([literal])
            return dpll_with_learning(new_clauses, assignment, unit_clause_stack, learned_clauses)
        literal = select_literal(clauses, assignment)
        new_clauses1 = [c for c in clauses if literal not in c]
        new_clauses2 = [c for c in clauses if -literal not in c]
        return dpll_with_learning(new_clauses1, assignment + [literal], unit_clause_stack, learned_clauses) or \
               dpll_with_learning(new_clauses2, assignment + [-literal], unit_clause_stack, learned_clauses)

    def find_pure_literal(clauses, assignment):
        for literal in range(1, max([abs(lit) for clause in clauses]) + 1):
            if literal not in assignment and -literal not in assignment:
                pure_literal = literal
                while True:
                    found = False
                    for clause in clauses:
                        if literal in clause:
                            found = True
                            break
                        if -literal in clause:
                            pure_literal = -pure_literal
                            found = True
                            break
                    if not found:
                        return pure_literal

    def find_pure_symbol(clauses, assignment):
        symbols = set()
        for clause in clauses:
            for literal in clause:
                symbols.add(abs(literal))
        for symbol in symbols:
            if symbol not in assignment and -symbol not in assignment:
                return symbol

    def find_unit_clause(clauses, assignment):
        for clause in clauses:
            if len([l for l in clause if l not in assignment and -l not in assignment]) == 1:
                literal = [l for l in clause if l not in assignment and -l not in assignment][0]
                return literal

    def select_literal(clauses, assignment):
        return random.choice([l for l in range(1, max([abs(lit) for clause in clauses]) + 1) if l not in assignment and -l not in assignment])

    assignment = [None] * (max([abs(lit) for clause in formula]) + 1)
    unit_clause_stack = []
    learned_clauses = []
    return len(learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    formula = generate_random_3cnf(n)
    S = list(range(1, n + 1))
    fourier_sum = sum(abs(fourier_coefficient(formula, [s])) for s in S)
    proof_length = resolution_length(formula)
    conjecture_holds = fourier_sum <= proof_length
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "resolution_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")