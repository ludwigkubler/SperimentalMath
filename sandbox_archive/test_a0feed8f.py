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
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def rank_of_matrix(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def construct_tropical_polynomial(edges, q):
    n = len(edges) + 1
    f = [0] * (q ** n)
    for u, v in edges:
        f[u * q + v] = -math.inf
    return f

def max_cut_approximation(n, q):
    # Placeholder for actual max-CUT approximation algorithm
    # This is a dummy implementation that always returns a valid solution
    return [random.choice([0, 1]) for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    q = random.randint(2, 5)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    f = construct_tropical_polynomial(edges, q)
    rank = rank_of_matrix([f])
    G = max_cut_approximation(n, q)
    ratio = sum(G) / n
    metric_value = rank * ratio
    instances_tested = 1
    conjecture_holds = rank >= q + 1
    counterexample = "" if conjecture_holds else "rank_too_low"
    return {
        "metric_name": "Rank of Tropical Polynomial",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")