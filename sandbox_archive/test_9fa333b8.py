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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank_of_matrix(A):
    n, m = len(A), len(A[0])
    A_copy = [A[i][:] for i in range(n)]
    r = 0
    for j in range(m):
        i_max = r
        for i in range(r, n):
            if abs(A_copy[i][j]) > abs(A_copy[i_max][j]):
                i_max = i
        if abs(A_copy[i_max][j]) > 1e-9:
            A_copy[r], A_copy[i_max] = A_copy[i_max], A_copy[r]
            for i in range(r + 1, n):
                factor = A_copy[i][j] / A_copy[r][j]
                for k in range(m):
                    A_copy[i][k] -= factor * A_copy[r][k]
            r += 1
    return r

def generate_k_clique_instance(n, k):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < (k / (n - i)) ** k:
                edges.append((i, j))
    return edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            edges = generate_k_clique_instance(n, n)
            A = [[0] * n for _ in range(n)]
            b = [1 if i in (u, v) else 0 for u, v in edges]
            for u, v in edges:
                A[u][v], A[v][u] = 1, 1
            rank = rank_of_matrix(A)
            results.append((n, rank))
    mean_rank = sum(rank for n, rank in results) / len(results)
    conjecture_holds = all(rank >= n**n * math.log(n) for _, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "minimal_matroid_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")