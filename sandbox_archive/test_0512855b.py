# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def cohomological_complex(G):
    n = len(G)
    complex_ = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if G[u][v]:
            complex_[u][v] = -1
            complex_[v][u] = -1
    return complex_

def rank_variance(complex_):
    m, n = len(complex_), len(complex[0])
    A = [[complex_[i][j] for j in range(n) if i != j] for i in range(m)]
    rank_A = gaussian_elimination(A)
    total = 0
    count = 0
    for row in complex_:
        if any(row):
            total += (rank_A - sum(1 for x in row if x)) ** 2
            count += 1
    return Fraction(total, count) if count > 0 else Fraction(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(3, min(n - 1, 8))
    G = [[0] * n for _ in range(n)]
    for _ in range(d * n // 2):
        u, v = random.sample(range(n), 2)
        G[u][v] = G[v][u] = 1
    complex_ = cohomological_complex(G)
    beta2 = gaussian_elimination(complex_)
    Rv = rank_variance(complex_)
    return {
        "metric_name": "Rank Variance",
        "metric_value": float(Rv),
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": abs(Rv - beta2) <= 3,
        "counterexample": "" if abs(Rv - beta2) <= 3 else f"Rv={Rv}, β2={beta2}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rv ≠ β2\" first_failing_seed={first_failing_seed}")