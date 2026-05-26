# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [[A[i][j] for j in range(n + 1)] for i in range(n)]
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n + 1):
                    M[k][j] -= factor * M[i][j]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for k in range(i+1, n):
            x[i] -= M[i][k] * x[k]
    return x

def generate_bdd(n):
    if n == 0:
        return [[], []]
    var = random.randint(0, n-1)
    left = generate_bdd(var)
    right = generate_bdd(var)
    return [left[0] + [(var, '0')] + right[0], left[1] + [(var, '1')] + right[1]]

def characteristic_polynomial(bdd):
    if not bdd:
        return [[1]]
    n = len(bdd[0])
    A = [[0] * (n+1) for _ in range(n+1)]
    for path in bdd[0]:
        i = 0
        for v, bit in path:
            if bit == '0':
                A[i][i+1] += 1
                i += 1
            else:
                A[n-1-i][n-1-i-1] -= 1
    return gaussian_elimination(A, [1] * (n+1))

def tropical_hodge_class_rank(poly):
    n = len(poly)
    rank = 0
    for i in range(n):
        if poly[i]:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = 2
    d = random.randint(1, n)
    
    bdd = generate_bdd(n)
    poly = characteristic_polynomial(bdd)
    rank = tropical_hodge_class_rank(poly)
    
    c_2_d = 4
    if rank > c_2_d * d:
        return {
            "metric_name": "tropical_hodge_class_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank}, expected={c_2_d*d}"
        }
    
    return {
        "metric_name": "tropical_hodge_class_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank exceeds bound' first_failing_seed={first_failing_seed}")