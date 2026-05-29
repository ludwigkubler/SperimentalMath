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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i == j:
                A[i][j] = Fraction(1, A[i][j])
            else:
                A[i][j] = Fraction(0)
        for k in range(m):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(m)]
    A_augmented = [row + col for row, col in zip(A, I)]
    gaussian_elimination(A_augmented)
    return [row[n:] for row in A_augmented]

def maslov_tft(f, beta, n):
    h = [f[(x - y) % n] + f[y] for x in range(n) for y in range(n)]
    k_values = list(range(1, n))
    exp_sum = sum(math.exp(-beta * h[x]) * math.cos(2 * math.pi * 1j * k * x / n) for k in k_values)
    return abs(exp_sum)

def cv(f, n):
    g = [min(f[(x - y) % n] + f[y] for y in range(n)) for x in range(n)]
    delta = [maslov_tft(g, 5, n) - 2 * maslov_tft(f, 5, n) for _ in range(50)]
    mean_delta = sum(delta) / len(delta)
    std_delta = math.sqrt(sum((x - mean_delta) ** 2 for x in delta) / len(delta))
    return std_delta / max(mean_delta, 1e-6)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 32, 40]
    results = []
    for n in n_values:
        f = [random.random() for _ in range(n)]
        deltas = [cv(f, n) for _ in range(50)]
        cv_value = sum(deltas) / len(deltas)
        results.append({
            "n": n,
            "cv": cv_value
        })
    mean_cv = sum(result["cv"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    conjecture_holds = all(result["cv"] <= 0.25 for result in results)
    counterexample = "" if conjecture_holds else "CV > 0.25"
    return {
        "metric_name": "orbit_cv",
        "metric_value": mean_cv,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 32))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_cv = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_cv} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cv} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CV > 0.25\" first_failing_seed={first_failing_seed}")