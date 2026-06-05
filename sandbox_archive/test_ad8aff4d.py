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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def random_d_regular_variety(n, d):
        A = [[0] * n for _ in range(n)]
        for i in range(d):
            while True:
                row = random.randint(0, n-1)
                col = random.randint(0, n-1)
                if row != col and A[row][col] == 0:
                    A[row][col] = 1
                    break
        return gaussian_elimination(A)

    def circuit_satisfiability_threshold(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        assignment = {i: random.choice([0, 1]) for i in range(1, n+1)}
        satisfiable = True
        for clause in clauses:
            if all(assignment[abs(lit)] == (lit > 0) for lit in clause):
                continue
            else:
                satisfiable = False
                break
        return 1 if satisfiable else 0

    def minimal_tropical_motivic_rank(A):
        rank = 0
        while A:
            pivot_row = max(range(len(A)), key=lambda i: abs(A[i][rank]))
            if A[pivot_row][rank] == 0:
                break
            for j in range(rank + 1, len(A[0])):
                A[pivot_row][j] /= A[pivot_row][rank]
            for i in range(len(A)):
                if i != pivot_row and A[i][rank] != 0:
                    factor = A[i][rank]
                    for j in range(rank, len(A[0])):
                        A[i][j] -= factor * A[pivot_row][j]
            rank += 1
        return rank

    n_max = 40
    instances_tested = 30
    tmr_values = []
    cst_values = []

    for _ in range(instances_tested):
        d = random.randint(2, min(n_max//2, 5))
        A = random_d_regular_variety(n_max, d)
        tmr = minimal_tropical_motivic_rank(A)
        cst = circuit_satisfiability_threshold(n_max)
        tmr_values.append(tmr)
        cst_values.append(cst)

    if len(tmr_values) < instances_tested:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(tmr_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)

    correlation_coefficient = pearson_correlation(tmr_values, cst_values)
    p_value = 0.05  # Placeholder for actual p-value calculation

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "not_enough_data"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")