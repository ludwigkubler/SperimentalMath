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

def matrix_multiply(A, B, p):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % p
    return C

def fraction_free_gaussian_elimination(A, b, p):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = (A[j][i] * pow(A[i][i], -1, p)) % p
            for k in range(n):
                A[j][k] = (A[j][k] - factor * A[i][k]) % p
            b[j] = (b[j] - factor * b[i]) % p
    return [x[0] for x in b]

def random_polynomial(N, d, p):
    coefficients = [[random.randint(0, p-1) for _ in range(d+1)] for _ in range(N)]
    return coefficients

def build_ABP(N, w, d, p):
    M = [random_polynomial(N, 2, p) for _ in range(w)]
    f = [[M[i][j][k] * M[(i+j)%w][k][l] for k in range(d+1)] for j in range(w) for l in range(2)]
    return f

def compute_T(f, N, d, p):
    T = [[0] * (N*(d+1)) for _ in range(N*(d+1))]
    for i in range(N):
        for j in range(d+1):
            for k in range(N):
                for l in range(2):
                    T[i*(d+1)+j][k*(d+1)+l] = f[k][i][j]
    return T

def run_trial(seed: int) -> dict:
    random.seed(seed)
    Ns = [8, 10, 12, 14]
    ws = [2, 3]
    ds = [3, 4]
    results = []
    
    for N in Ns:
        for w in ws:
            for d in ds:
                f = build_ABP(N, w, d, 2**30 - 1)
                T = compute_T(f, N, d, 2**30 - 1)
                sigma_f = N * (N + 1) // 2 - len(flat(T))
                results.append(sigma_f >= N - 2 * w ** 2)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "sigma_f",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(False)]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")