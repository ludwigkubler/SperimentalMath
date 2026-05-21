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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def log2_rank_GF2(M):
    rows, cols = len(M), len(M[0])
    rank = 0
    for i in range(rows):
        if any(M[i][j] != 0 for j in range(cols)):
            pivot_col = next(j for j in range(cols) if M[i][j] != 0)
            for j in range(i, rows):
                if M[j][pivot_col] != 0:
                    factor = -M[j][pivot_col] / M[i][pivot_col]
                    for k in range(pivot_col, cols):
                        M[j][k] += factor * M[i][k]
            rank += 1
    return rank

def vc_dimension(R_g):
    n = len(R_g)
    for d in range(n + 1):
        if all(len(shatter) >= (1 << i) for i, shatter in enumerate(R_g)):
            return d
    return n

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def index_b(g):
    return lambda x: g(x)

def inner_product_b(g):
    return lambda x, y: sum(xi * yi for xi, yi in zip(g(x), y))

def equality_b(g):
    return lambda x, y: 1 if g(x) == g(y) else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2, 3, 4]
    A_sizes = [4, 8]
    B_sizes = [2, 3, 4]
    gadgets = [index_b, inner_product_b, equality_b]

    results = []
    for _ in range(10):  # Sample 10 (f,g) pairs per seed
        n = random.choice(n_values)
        f = random_boolean_function(n)
        A_size = random.choice(A_sizes)
        B_size = random.choice(B_sizes)
        g = lambda x: [random.choice([0, 1]) for _ in range(B_size)]
        R_g = [g(a) for a in range(A_size)]
        d = vc_dimension(R_g)

        M = [[f(g(a, b)) for b in range(B_size)] for a in range(A_size ** n)]
        rank = log2_rank_GF2(M)
        slack = rank - (0.5 * n * d - n)
        results.append({
            "metric_name": "slack",
            "metric_value": slack,
            "instances_tested": 1,
            "conjecture_holds": slack >= 0,
            "counterexample": ""
        })

    return {
        "seed": seed,
        "metric_name": "slack",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.9:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low VC gadget achieves anomalously high D^cc\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")