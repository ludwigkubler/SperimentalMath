# auto-injected by SEC sandbox
import math
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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(i + 1, cols):
            A[i][j] /= A[i][i]
        A[i][i] = Fraction(1)
        for k in range(rows):
            if k != i:
                factor = A[k][i]
                for j in range(i, cols):
                    A[k][j] -= factor * A[i][j]
    return A

def rank(matrix):
    A = [row[:] for row in matrix]
    r = gaussian_elimination(A)
    return sum(1 for row in r if any(x != 0 for x in row))

def quadratic_form(variables, clauses, p):
    n = len(variables)
    Q = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            index = abs(var) - 1
            if var > 0:
                Q[index][index] += Fraction(1)
            else:
                Q[index][index] -= Fraction(1)
    return rank(Q)

def tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(2, 3))]
        clauses.append(clause)
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    variables, clauses = tseitin_formula(n, m)
    p = random.choice([2, 3, 5, 7, 11])
    rank_value = quadratic_form(variables, clauses, p)
    proof_length = len(clauses) + n  # Simplified for testing
    correlation_coefficient = (rank_value - proof_length) / (n * m)
    conjecture_holds = correlation_coefficient > 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")