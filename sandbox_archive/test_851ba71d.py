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
from fractions import Fraction
from math import sqrt

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return [sum(row) for row in A]

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    var = next(iter(cnf))
    pos_clauses = [c for c in cnf if var in c]
    neg_clauses = [c for c in cnf if -var in c]
    if any(not dpll(clause, assignment) for clause in neg_clauses):
        return dpll(pos_clauses, {**assignment, var: True})
    elif any(not dpll(clause, assignment) for clause in pos_clauses):
        return dpll(neg_clauses, {**assignment, var: False})
    else:
        return False

def lcai(cnf):
    n = len(cnf)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            pos_clauses_i = [c for c in cnf if i+1 in c]
            neg_clauses_i = [c for c in cnf if -(i+1) in c]
            pos_clauses_j = [c for c in cnf if j+1 in c]
            neg_clauses_j = [c for c in cnf if -(j+1) in c]
            A[i][j] = len(pos_clauses_i & pos_clauses_j) - len(neg_clauses_i & neg_clauses_j)
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    lcai_values = []
    dpll_heights = []

    for _ in range(instances_tested):
        cnf = [[random.randint(1, n_max) for _ in range(random.randint(2, 5))] for _ in range(n_max)]
        lcai_value = lcai(cnf)
        dpll_height = len(dpll(cnf))
        lcai_values.append(lcai_value)
        dpll_heights.append(dpll_height)

    correlation_coefficient = sum((x - mean(x)) * (y - mean(y)) for x, y in zip(lcai_values, dpll_heights)) / (len(lcai_values) * sqrt(variance(lcai_values)) * sqrt(variance(dpll_heights)))
    mean_difference = mean([abs(x - y) for x, y in zip(lcai_values, dpll_heights)])

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def variance(values):
    avg = mean(values)
    return sum((x - avg) ** 2 for x in values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = mean([r["metric_value"] for r in results])
    std_value = sqrt(variance([r["metric_value"] for r in results]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")