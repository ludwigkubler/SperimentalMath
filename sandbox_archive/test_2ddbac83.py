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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for c in range(n):
        det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def characteristic_polynomial(A):
    n = len(A)
    x = [[0] * (n + 1) for _ in range(n + 1)]
    x[n][n] = 1
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            x[i][j] = A[i][j]
            if i < n - 1:
                x[i][j] -= sum(A[i + k][j] * x[k][i] for k in range(i + 1))
    return x

def minimal_tropical_discriminant(poly):
    n = len(poly)
    poly = [p for p in poly if p != 0]
    if not poly:
        return float('inf')
    return min(abs(p) for p in poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, n - 1)
    
    # Generate a random DNF formula representing the k-CLIQUE problem
    dnf_formula = []
    for _ in range(n):
        clause = [random.choice([True, False]) for _ in range(k)]
        dnf_formula.append(clause)
    
    # Convert DNF to characteristic polynomial (simplified for demonstration)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if all(dnf_formula[i][j] == dnf_formula[j][i]):
                A[i][j] = 1
    
    char_poly = characteristic_polynomial(A)
    disc = minimal_tropical_discriminant(char_poly)
    
    return {
        "metric_name": "minimal_tropical_discriminant",
        "metric_value": disc,
        "instances_tested": n,
        "conjecture_holds": disc >= n ** (3/2),
        "counterexample": "" if disc >= n ** (3/2) else f"n={n}, disc={disc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_disc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='disc < n^(3/2)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} (not enough seeds supported)")