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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det
    
    def characteristic_polynomial(A):
        n = len(A)
        x = random.random()  # Placeholder for variable x
        poly = [1]
        for i in range(n):
            coeff = sum(A[i][j] * (-x)**(n-j-1) for j in range(n)) / math.factorial(n-i-1)
            poly.append(coeff)
        return poly
    
    def minimal_root_separation(poly):
        roots = []
        for _ in range(10):  # Simple root-finding method
            x0, x1 = random.uniform(-10, 10), random.uniform(-10, 10)
            while abs(x1 - x0) > 1e-6:
                f_x0, f_x1 = poly[0], poly[0]
                for i in range(1, len(poly)):
                    f_x0 += poly[i] * x0**i
                    f_x1 += poly[i] * x1**i
                df_x0 = sum(i * poly[i] * x0**(i-1) for i in range(1, len(poly)))
                x0, x1 = x1, x1 - f_x1 / df_x0
            roots.append(x1)
        return min(abs(r1 - r2) for r1, r2 in combinations(roots, 2))
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def characteristic_matrix_pencil(cnf):
        n = len(cnf)
        A = [[0] * (n+1) for _ in range(n+1)]
        B = [[0] * (n+1) for _ in range(n+1)]
        for i, clause in enumerate(cnf):
            A[i][i] = -len(clause)
            for literal in clause:
                j = abs(literal) - 1
                if literal > 0:
                    B[j][i] += 1
                else:
                    B[i][j] += 1
        return A, B
    
    def log_size(P):
        return math.log(len(P))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_random_cnf(n)
    A, B = characteristic_matrix_pencil(cnf)
    char_poly = characteristic_polynomial(A - x * B)
    min_separation = minimal_root_separation(char_poly)
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": log_size(cnf) <= min_separation and min_separation <= log_size(cnf) + 3,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")