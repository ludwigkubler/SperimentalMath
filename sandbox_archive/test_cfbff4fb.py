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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rref = gaussian_elimination([row[:] for row in matrix])
    rank = 0
    for row in rref:
        if any(row[i] != Fraction(0) for i in range(len(row))):
            rank += 1
    return rank

def dpll(formula, assignment={}):
    if not formula:
        return True
    if len(formula) == 1:
        clause = formula[0]
        if all(var in assignment and assignment[var] == val for var, val in clause.items()):
            return False
        if any(var not in assignment for var in clause):
            var = next(var for var in clause if var not in assignment)
            return dpll(formula + [{var: True}], assignment) or dpll(formula + [{var: False}], assignment)
    unit_clause = next((clause for clause in formula if len(clause) == 1), None)
    if unit_clause:
        var, val = list(unit_clause.items())[0]
        return dpll(formula + [{var: not val}], assignment)
    pure_literal = next((var for var in set().union(*formula) if sum(var in clause and val == (clause[var] if isinstance(clause, dict) else True) for clause in formula) - sum(-var in clause and val == (not clause[-var] if isinstance(clause, dict) else False) for clause in formula) != 0), None)
    if pure_literal:
        return dpll(formula + [{pure_literal: True}], assignment) or dpll(formula + [{pure_literal: False}], assignment)
    var = next(iter(set().union(*formula)))
    return dpll(formula + [{var: True}], assignment) or dpll(formula + [{var: False}], assignment)

def mrd(formula):
    n = len(formula)
    matrix = [[0] * n for _ in range(n)]
    for i, clause in enumerate(formula):
        for var, val in clause.items():
            if isinstance(var, int) and 1 <= var <= n:
                j = var - 1
                if val:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = -1
    return rank(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        variables = list(range(1, n+1))
        clauses = [{random.choice(variables): random.choice([True, False])} for _ in range(n)]
        formula = {tuple(clause.items()) for clause in clauses}
        mrd_value = mrd(formula)
        dpll_height = len(dpll(formula))
        results.append((mrd_value, dpll_height))
    mean_mrd = sum(mrd for mrd, _ in results) / len(results)
    mean_dpll = sum(dpll for _, dpll in results) / len(results)
    correlation_coefficient = sum((mrd - mean_mrd) * (dpll - mean_dpll) for mrd, dpll in results) / (len(results) * math.sqrt(sum((mrd - mean_mrd)**2 for mrd, _ in results)) * math.sqrt(sum((dpll - mean_dpll)**2 for _, dpll in results)))
    conjecture_holds = abs(correlation_coefficient) > 0.1
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mrd={mean_mrd}, dpll={mean_dpll}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_result = sum(results) / len(results)
    std_result = math.sqrt(sum((x - mean_result)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) > 0.1) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_result} std={std_result} support_fraction={support_fraction}")
    elif any(abs(r) <= 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result) <= 0.1)
        print(f"RESULT: FALSIFIED counterexample=\"mrd and dpll are not significantly correlated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")