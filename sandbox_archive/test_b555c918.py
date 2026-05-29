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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def min_plus_self_convolution(f, n):
    g = [0] * n
    for x in range(n):
        g[x] = min(f[y] + f[(x - y) % n] for y in range(n))
    return g

def maslov_tft(h, beta, n):
    k_values = list(range(-n // 2, n // 2 + 1))
    tft = [0] * len(k_values)
    for x in range(n):
        exp_sum = sum(math.exp(-beta * h[x]) * math.exp(-2 * math.pi * 1j * k * x / n) for k in k_values)
        tft[k_values.index(k)] += abs(exp_sum)
    return tft

def mfc(h):
    return min(abs(tft[k]) for k in range(1, len(tft)))

def cv(f, n):
    sigma = [i for i in range(n)]
    random.shuffle(sigma)
    g = min_plus_self_convolution(f, n)
    h = maslov_tft(g, 5, n)
    delta = abs(mfc(h) - 2 * mfc(f))
    return delta

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 12, 16, 20, 24, 32, 40]:
        f = [random.random() for _ in range(n)]
        deltas = [cv(f, n) for _ in range(50)]
        mean_delta = sum(deltas) / len(deltas)
        std_delta = math.sqrt(sum((d - mean_delta) ** 2 for d in deltas) / len(deltas))
        cv_value = std_delta / max(mean_delta, 1e-6)
        results.append(cv_value)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(cv_value <= 0.25 for cv_value in results)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    return {
        "metric_name": "orbit_coefficient_of_variation",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max([8, 12, 16, 20, 24, 32, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")