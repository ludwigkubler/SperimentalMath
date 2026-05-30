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
    
    def generate_k_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x for x in clause}
            else:
                clause = {-x for x in clause}
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(clauses):
        poly = [0] * (len(clauses) + 1)
        poly[0] = 1
        for clause in clauses:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (1 - x[literal])
                else:
                    term *= (1 + x[-literal])
            poly += [term]
        return poly

    def companion_matrix(poly):
        n = len(poly) - 1
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i + 1] = 1
        for i in range(n):
            A[n-1-i][0] = -poly[i]
        return A

    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for k in range(m):
            max_row = k
            for i in range(k+1, m):
                if abs(A[i][k]) > abs(A[max_row][k]):
                    max_row = i
            A[k], A[max_row] = A[max_row], A[k]
            b[k], b[max_row] = b[max_row], b[k]
            for i in range(k+1, m):
                factor = A[i][k] / A[k][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                b[i] -= factor * b[k]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        if n == 1:
            return [matrix[0][0]]
        if n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            return [(a + d) / 2 + math.sqrt((a + d)**2 - 4 * (a*d - b*c)) / 2,
                    (a + d) / 2 - math.sqrt((a + d)**2 - 4 * (a*d - b*c)) / 2]
        A = matrix
        x = [1] * n
        for _ in range(100):
            Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            x = [x_i / sum(abs(x_j) for x_j in Ax) for x_i in Ax]
        return x

    def distinct_roots(eigenvals):
        return len(set(eigenvals))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):
            m = random.randint(n, n * 2)
            clauses = generate_k_cnf(n, m)
            poly = clause_indicator_polynomial(clauses)
            A = companion_matrix(poly)
            eigenvals = eigenvalues(A)
            num_roots = distinct_roots(eigenvals)
            results.append(num_roots)
            total_instances += 1
            max_n = max(max_n, n)

    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    conjecture_holds = all(0.5 * m**(1/3) * n**(2/3) <= x <= 2 * m**(1/3) * n**(2/3) for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "distinct_roots",
        "metric_value": mean_value,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")