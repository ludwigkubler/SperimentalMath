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

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    det = 0
    if n == 1:
        return [[1 / A[0][0]]]
    
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** (i % 2)
        det += sign * A[0][i] * matrix_det(submatrix)
    
    inv = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1) ** ((i + j) % 2)
            inv[i][j] = sign * matrix_det(submatrix) / det
    
    return inv

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    
    det = 0
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** (i % 2)
        det += sign * A[0][i] * matrix_det(submatrix)
    
    return det

def geometric_entropy(Q):
    n = len(Q)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    Q_inv = matrix_inv(Q)
    H = -sum(sum(Q[i][j] * math.log2(Q[i][j]) for j in range(n)) for i in range(n))
    return H

def disjointness_complexity(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return 1 + disjointness_complexity(n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    Q = [[random.random() for _ in range(n)] for _ in range(n)]
    gamma_Q = geometric_entropy(Q)
    kappa_DISJ_n = disjointness_complexity(n)
    instances_tested = 1
    conjecture_holds = gamma_Q >= kappa_DISJ_n
    counterexample = "" if conjecture_holds else f"gamma_Q={gamma_Q}, kappa_DISJ_n={kappa_DISJ_n}"
    return {
        "metric_name": "geometric_entropy",
        "metric_value": gamma_Q,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gamma_Q = sum(r["metric_value"] for r in results) / len(results)
    std_gamma_Q = math.sqrt(sum((r["metric_value"] - mean_gamma_Q) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gamma_Q} std={std_gamma_Q} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gamma_Q < kappa_DISJ_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")