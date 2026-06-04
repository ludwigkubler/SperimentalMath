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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, C):
        clauses = set()
        while len(clauses) < C:
            clause = []
            for _ in range(2):  # Each clause has exactly 2 literals
                var = random.randint(1, n)
                sign = random.choice([-1, 1])
                clause.append((var, sign))
            clauses.add(tuple(sorted(clause)))
        return clauses

    def cnf_to_density_matrix(cnf):
        n = max(var for _, var in cnf) if cnf else 0
        M = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, (_, var_i) in enumerate(clause):
                for j, (_, var_j) in enumerate(clause):
                    if i < j:
                        M[var_i][var_j] += Fraction(1)
                        M[var_j][var_i] += Fraction(1)
        return M

    def geometric_entanglement(M):
        n = len(M) - 1
        det_M = determinant(M, n)
        det_I_n_minus_1 = determinant(identity_matrix(n), n - 1)
        return abs(det_M / det_I_n_minus_1)

    def identity_matrix(n):
        return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

    def determinant(M, n):
        if n == 1:
            return M[0][0]
        det = Fraction(0)
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for row in M[1:]]
            sign = (-1) ** c
            det += sign * M[0][c] * determinant(submatrix, n - 1)
        return det

    def clause_set_complexity(cnf):
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    C_values = [random.randint(1, min(n-1, 40)) for _ in range(30)]
    
    E_values = []
    C_values_used = []

    for n in n_values:
        for C in C_values:
            cnf = generate_cnf(n, C)
            M = cnf_to_density_matrix(cnf)
            E = geometric_entanglement(M)
            E_values.append(E)
            C_values_used.append(C)

    correlation_coefficient = pearson_correlation(E_values, C_values_used)
    mean_difference = sum(abs(e - c) for e, c in zip(E_values, C_values_used)) / len(E_values)

    return {
        "metric_name": "geometric_entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and mean_difference <= 3,
        "counterexample": "" if correlation_coefficient > 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

def pearson_correlation(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y2 = sum(yi ** 2 for yi in y)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5

    if denominator == 0:
        return 0

    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]

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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")