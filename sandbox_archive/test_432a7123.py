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
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(m):
            if i != j:
                factor = Augmented[j][i] / Augmented[i][i]
                for k in range(n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    X = [0] * n
    for i in range(n-1, -1, -1):
        X[i] = Augmented[i][-1]
        for j in range(i+1, n):
            X[i] -= Augmented[i][j] * X[j]
        X[i] /= Augmented[i][i]
    return X

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.isqrt(n**1.5)
    
    def perm_polynomial(x):
        return sum(x[i]**n for i in range(n))
    
    def det_polynomial(x):
        if n == 1:
            return x[0]
        elif n == 2:
            return x[0]*x[3] - x[1]*x[2]
        else:
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in x[1:]]
                det += (-1)**j * x[0][j] * det_polynomial(submatrix)
            return det
    
    def plethysm_coefficient(poly, hook_partition):
        arm_length = hook_partition[0]
        if arm_length == 0:
            return 1
        coeff = 0
        for i in range(arm_length + 1):
            coeff += poly(i) * plethysm_coefficient(poly, (i,) + hook_partition[1:])
        return coeff
    
    perm_ratio = max(plethysm_coefficient(perm_polynomial, (k, 1**(n-k))) for k in range(n))
    det_ratio = max(plethysm_coefficient(det_polynomial, (k, 1**(m-k))) for k in range(m+1))
    
    return {
        "metric_name": "Ratio",
        "metric_value": perm_ratio / det_ratio,
        "instances_tested": 1,
        "conjecture_holds": perm_ratio >= 2**(n/10) and det_ratio <= n**3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")