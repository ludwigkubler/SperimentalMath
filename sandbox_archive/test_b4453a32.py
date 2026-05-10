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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def tropical_convex_hull(poly):
    n = len(poly)
    hull = []
    for i in range(n):
        if all(poly[i][j] <= poly[j][i] for j in range(n) if j != i):
            hull.append(i)
    return hull

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    clauses = [random.sample(variables, 3) for _ in range(n)]
    poly = [[-math.inf]*n for _ in range(n)]
    for clause in clauses:
        for i in clause:
            poly[i][i] = 0
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                poly[i][j] = min(poly[i][j], poly[j][i])
                poly[j][i] = min(poly[i][j], poly[j][i])
            else:
                poly[i][j] = max(poly[i][j], poly[j][i])
                poly[j][i] = max(poly[i][j], poly[j][i])
    hull = tropical_convex_hull(poly)
    metric_value = len(hull)
    instances_tested = 1
    conjecture_holds = metric_value >= math.log(n, 2)
    counterexample = "" if conjecture_holds else f"n={n}, extreme_points={metric_value}"
    return {
        "metric_name": "extreme_points",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, extreme_points={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)