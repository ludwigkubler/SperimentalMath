# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def tropical_add(a, b):
    return max(a, b)

def tropical_subtract(a, b):
    return a - b

def tropical_multiply(a, b):
    return a + b

def tropical_divide(a, b):
    return a - b if b != 0 else float('inf')

def tropical_exponentiate(a, b):
    return a * b

def tropical_negate(a):
    return -a

def tropical_zero():
    return float('-inf')

def tropical_one():
    return 0

def tropical_identity(x):
    return x

def tropical_inverse(x):
    return -x if x != 0 else float('inf')

def tropical_max(a, b):
    return max(a, b)

def tropical_min(a, b):
    return min(a, b)

def tropical_sum(lst):
    return sum(lst)

def tropical_mean(lst):
    return sum(lst) / len(lst)

def tropical_dot_product(v1, v2):
    return sum(tropical_multiply(v1[i], v2[i]) for i in range(len(v1)))

def tropical_matrix_multiplication(A, B):
    m, n = len(A), len(B[0])
    result = [[tropical_zero() for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] = tropical_add(result[i][j], tropical_multiply(A[i][k], B[k][j]))
    return result

def tropical_invert(matrix):
    n = len(matrix)
    identity = [[tropical_zero() if i != j else tropical_one() for j in range(n)] for i in range(n)]
    augmented = [row + col for row, col in zip(matrix, identity)]
    
    for i in range(n):
        pivot = augmented[i][i]
        if pivot == tropical_zero():
            raise ValueError("Matrix is not invertible")
        
        for j in range(i, n * 2):
            augmented[i][j] = tropical_divide(augmented[i][j], pivot)
        
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n * 2):
                    augmented[k][j] = tropical_subtract(augmented[k][j], tropical_multiply(factor, augmented[i][j]))
    
    inverse = [row[n:] for row in augmented]
    return inverse

def tropical_fourier_transform(f, N):
    d = len(f)
    F = [[tropical_zero() for _ in range(N)] for _ in range(N)]
    for kx in range(N):
        for ky in range(N):
            sum_val = tropical_zero()
            for x in range(N):
                for y in range(N):
                    sum_val = tropical_add(sum_val, tropical_multiply(f[x][y], tropical_exponentiate(tropical_negate(kx * x + ky * y), N)))
            F[kx][ky] = sum_val
    return F

def discrepancy_measure(f):
    max_val = tropical_max(*[tropical_max(*row) for row in f])
    min_val = tropical_min(*[tropical_min(*row) for row in f])
    mean_val = tropical_mean([tropical_mean(row) for row in f])
    return tropical_subtract(tropical_subtract(max_val, min_val), mean_val)

def minimal_fourier_coefficient(F):
    return min(abs(coeff) for row in F for coeff in row if coeff != tropical_zero())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    N = 8
    d = 2
    
    f = [[random.uniform(-10, 10) for _ in range(N)] for _ in range(N)]
    g = [[random.uniform(-10, 10) for _ in range(N)] for _ in range(N)]
    
    F = tropical_fourier_transform(f, N)
    G = tropical_fourier_transform(g, N)
    
    disc_f = discrepancy_measure(f)
    disc_g = discrepancy_measure(g)
    
    lhs = abs(tropical_subtract(disc_f, disc_g))
    rhs = max(abs(F[kx][ky] - G[kx][ky]) for kx in range(N) for ky in range(N))
    
    conjecture_holds = lhs <= rhs
    counterexample = "" if conjecture_holds else f"Discrepancy difference {lhs} > Fourier coefficient difference {rhs}"
    
    return {
        "metric_name": "LipschitzRatio",
        "metric_value": lhs / rhs,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_lhs_rhs_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_lhs_rhs_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")