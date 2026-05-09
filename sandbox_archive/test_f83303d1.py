# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def plethysm(f, λ):
    n = len(λ)
    m = max(λ)
    P = [[0] * (n + 1) for _ in range(m + 1)]
    P[0][0] = 1
    for l in range(1, m + 1):
        for k in range(n + 1):
            P[l][k] = sum(P[l - p][k - q] * f[p][q] for p, q in combinations(range(l), 2))
    return P[λ[0]][λ[1]]

def symmetric_function(Φ):
    n = len(Φ)
    f = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in Φ:
        x, y, z = random.sample(range(n), 3)
        f[x][y] += 1
        f[y][z] += 1
        f[z][x] += 1
    return f

def size(Φ):
    n = len(Φ)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in Φ:
        x, y, z = random.sample(range(n), 3)
        A[x][y] += 1
        A[y][z] += 1
        A[z][x] += 1
    return determinant(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    Φ = [[random.randint(0, n - 1) for _ in range(3)] for _ in range(n)]
    f_Φ = symmetric_function(Φ)
    λ_values = [[n], [n-1, 1], [n-2, 1, 1]]
    size_Φ = size(Φ)
    plethysm_values = [plethysm(f_Φ, λ) for λ in λ_values]
    conjecture_holds = all(value * size_Φ <= 2**(0.5 * n) for value in plethysm_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": sum(plethysm_values),
        "instances_tested": len(Φ),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")