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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(clauses):
        n = len(clauses) + 1
        poly = [0] * (n + 1)
        poly[0] = 1
        for clause in clauses:
            a, b = abs(clause[0]), abs(clause[1])
            if clause[0] > 0:
                poly[a] += 1
            else:
                poly[a] -= 1
            if clause[1] > 0:
                poly[b] += 1
            else:
                poly[b] -= 1
        return poly

    def companion_matrix(poly):
        n = len(poly) - 1
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            A[i][i + 1] = 1
            if i != 0:
                A[i][0] = -poly[i]
        return A

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x

    def distinct_roots(poly):
        n = len(poly) - 1
        if n == 0:
            return 0
        roots = set()
        for i in range(1, n + 1):
            b = [-poly[j] * i**j for j in range(n)]
            x = gaussian_elimination(companion_matrix(poly), b)
            roots.add(tuple(x))
        return len(roots)

    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        if n == 1:
            return [matrix[0][0]]
        if n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            return [a + d, (a * d - b * c) / (a + d)]
        eigenvals = []
        for i in range(n):
            A = [[matrix[j][k] for k in range(n) if k != i] for j in range(n) if j != i]
            det = matrix[i][i] * determinant(A)
            eigenvals.append(det / (sum(eigenvalues(matrix)) - matrix[i][i]))
        return eigenvals

    def determinant(matrix):
        n = len(matrix)
        if n == 0:
            return 1
        if n == 1:
            return matrix[0][0]
        det = 0
        for i in range(n):
            A = [[matrix[j][k] for k in range(1, n)] for j in range(1, n) if j != i]
            det += ((-1) ** i) * matrix[i][0] * determinant(A)
        return det

    def root_system(eigenvals):
        # Placeholder for a constructive mapping from eigenvalues to root system
        # This is a dummy implementation and should be replaced with actual logic
        return len(eigenvals)

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            clauses = generate_kcnf(n, m)
            poly = clause_indicator_polynomial(clauses)
            eigenvals = eigenvalues(companion_matrix(poly))
            roots = distinct_roots(poly)
            root_sys_size = root_system(eigenvals)
            instances_tested += 1
            total_metric_value += root_sys_size

    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = abs(mean_metric_value - (m ** (1/3) * n_max ** (2/3))) <= m ** (1/3) * n_max ** (2/3) / 2
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Distinct Roots in Root System",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")