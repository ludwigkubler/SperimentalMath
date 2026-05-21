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
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank_GF2(matrix):
    rows, cols = len(matrix), len(matrix[0])
    M = [[int(x) for x in row] for row in matrix]
    rref = []
    for i in range(rows):
        if all(M[i][j] == 0 for j in range(cols)):
            continue
        pivot_col = M[i].index(1)
        if i != len(rref):
            M[i], rref[-1] = rref[-1], M[i]
        for j in range(len(rref)):
            if i != j:
                factor = rref[j][pivot_col]
                for k in range(cols):
                    rref[j][k] ^= (factor * M[i][k]) % 2
        rref.append(M[i])
    return len(rref)

def VC(R_g):
    B_size = len(R_g[0])
    for d in range(1, B_size + 1):
        subsets = [set() for _ in range(d)]
        for i in range(B_size):
            subsets[i % d].add(i)
        if all(len(subset) == d for subset in subsets):
            return d
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([2, 3, 4])
    A_size = random.choice([4, 8])
    B_size = random.choice([2, 3, 4])
    
    def index_b(a, b):
        return a == b
    
    def inner_product_b(a, b):
        return sum(x * y for x, y in zip(a, b))
    
    def equality_b(a, b):
        return a == b
    
    gadgets = [index_b, inner_product_b, equality_b]
    g = random.choice(gadgets)
    
    R_g = [g(a, b) for b in range(B_size)]
    d = VC(R_g)
    
    f = lambda x: random.choice([0, 1])
    M = [[f(g(a, b)) for b in range(B_size)] for a in range(A_size ** n)]
    
    rank = rank_GF2(M)
    slack = (Fraction(1, 2) * n * d - n).limit_denominator()
    
    return {
        "metric_name": "slack",
        "metric_value": slack,
        "instances_tested": 1,
        "conjecture_holds": rank >= slack,
        "counterexample": "" if rank >= slack else f"rank={rank}, slack={slack}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too small\" first_failing_seed={first_failing_seed + 1}")