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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
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
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def svd(A):
    U, S, Vt = [], [], []
    m, n = len(A), len(A[0])
    Q, R = A, [[0]*n for _ in range(n)]
    for k in range(min(m, n)):
        u = [x / math.sqrt(sum(x**2 for x in Q[i])) for i in range(m)]
        U.append(u)
        Q = [[Q[i][j] - u[i] * R[j][k] for j in range(k, n)] for i in range(m)]
        r = sum(Q[i][k]**2 for i in range(m))
        S.append(math.sqrt(r))
        R[k][k] = math.sqrt(r)
    Vt = [[0]*m for _ in range(n)]
    for k in range(min(m, n)):
        v = [Q[i][k] / S[k] if j == k else 0 for i in range(m) for j in range(n)]
        Vt[k] = v
    return U, S, Vt

def frobenius_norm(M):
    return math.sqrt(sum(sum(x**2 for x in row) for row in M))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.randint(0, 1) if i == j else 0 for j in range(n)] for i in range(n)]
    rank = sum(1 for s in svd(M)[1] if abs(s) > 1e-6)
    norm = frobenius_norm(M)
    instances_tested = 1
    conjecture_holds = norm >= 0.9 * math.sqrt(n)
    counterexample = "" if conjecture_holds else "norm < 0.9√n"
    return {
        "metric_name": "Frobenius Norm",
        "metric_value": norm,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm < 0.9√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")