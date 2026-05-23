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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    k2, n = len(B[0]), len(B[0][0])
    C = [[[0 for _ in range(n)] for _ in range(k2)] for _ in range(m)]
    for i in range(m):
        for j in range(k2):
            for l in range(k):
                C[i][j][l] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def random_partial_function(n):
    domain = list(range(n))
    codomain = [0, 1]
    return {x: random.choice(codomain) for x in domain}

def tropicalize(f):
    n = len(f)
    T = [[[float('inf')] * (n + 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        T[i][i][0] = f[i]
    for k in range(1, n + 1):
        for i in range(n):
            for j in range(n):
                T[i][j][k] = min(T[i][j][k-1], T[i][k-1][k-1] + T[k-1][j][k-1])
    return T

def hodge_rank(T):
    n = len(T)
    H = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                H[i][j][k] = T[i][j][k]
    rank = 0
    for d in range(1, n + 1):
        if any(all(H[i][j][d] == float('inf') for i in range(n)) for j in range(n)):
            continue
        rank += 1
        for i in range(n):
            for j in range(n):
                if H[i][j][d] != float('inf'):
                    for k in range(n):
                        H[k][i][d-1] = min(H[k][i][d-1], H[k][j][d] + H[j][i][d])
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = random_partial_function(n)
        T = tropicalize(f)
        rank = hodge_rank(T)
        communication_complexity = n  # Placeholder for actual complexity calculation
        results.append({
            "n": n,
            "rank": rank,
            "communication_complexity": communication_complexity
        })
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["rank"] >= result["n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Hodge Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")