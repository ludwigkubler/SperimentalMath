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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def construct_group(category):
    n = len(category)
    A = [[0]*n for _ in range(n)]
    b = [0]*n
    for i in range(n):
        for j in range(n):
            if category[i][j]:
                A[i][j] = 1
                b[j] += 1
    try:
        x = gaussian_elimination(A, b)
    except ZeroDivisionError:
        return None
    G = [set() for _ in range(n)]
    for i in range(n):
        if x[i]:
            G[i].add(i)
    return G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    category = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    G = construct_group(category)
    if not G:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": None,
            "instances_tested": n*n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    rank = sum(len(g) for g in G)
    s = sum(category[i][j] for i in range(n) for j in range(n))
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": n*n,
        "conjecture_holds": rank <= s,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 31))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")