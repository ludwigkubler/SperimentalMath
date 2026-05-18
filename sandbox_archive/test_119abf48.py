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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def svd(A):
    m, n = len(A), len(A[0])
    U = [[0]*n for _ in range(m)]
    S = [0]*min(m, n)
    Vt = [[0]*m for _ in range(n)]
    
    # Compute A^T * A
    ATA = [[sum(A[i][k] * A[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
    
    # Perform QR decomposition on A^T * A
    Q, R = qr(ATA)
    
    # Compute SVD from QR decomposition
    U = [[Q[i][j] if j < m else 0 for j in range(n)] for i in range(m)]
    S = [R[j][j] for j in range(min(m, n))]
    Vt = R
    
    return U, S, Vt

def qr(A):
    m, n = len(A), len(A[0])
    Q = [[A[i][j] for j in range(n)] for i in range(m)]
    R = [[A[i][j] if i <= j else 0 for j in range(n)] for i in range(m)]
    
    for k in range(min(m, n)):
        norm = sum(A[i][k]**2 for i in range(k, m))**0.5
        Q[k][k] /= norm
        R[k][k] = norm
        
        for j in range(k+1, n):
            R[k][j] = sum(Q[i][k] * A[i][j] for i in range(k, m))
        
        for i in range(k+1, m):
            Q[i][k] /= R[k][k]
            
            for j in range(k, n):
                Q[i][j] -= Q[i][k] * R[k][j]
    
    return Q, R

def run_trial(seed: int) -> dict:
    random.seed(seed)
    sizes = [8, 16, 32]
    ensembles = [
        lambda N: [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)],
        lambda N: [[1 if (i + j) % 2 == 0 else -1 for i in range(N)] for j in range(N)],
        lambda N: [[1 if i == j else 0 for i in range(N)] for j in range(N)],
        lambda N, k: [[random.choice([-1, 1]) for _ in range(k)] for _ in range(k)] + \
                      [[0] * k + [random.choice([-1, 1])] + [0] * (N - k - 1) for _ in range(N - k)],
        lambda N: [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    ]
    
    min_ratio = float('inf')
    counterexample = ""
    
    for N in sizes:
        if N > 30:
            break
        M = ensembles[random.randint(0, len(ensembles) - 1)](N)
        U, S, Vt = svd(M)
        
        for r in [2, 3, 4]:
            max_det = 0
            for _ in range(2000):
                rows = random.sample(range(N), r)
                cols = random.sample(range(N), r)
                submatrix = [[M[i][j] for j in cols] for i in rows]
                det = abs(determinant(submatrix))
                max_det = max(max_det, det)
            
            D_r = max_det ** (2 / r)
            sigma_r_squared = S[r-1]**2
            ratio = 4 * sigma_r_squared / D_r
            
            if ratio < min_ratio:
                min_ratio = ratio
                counterexample = f"(N={N}, r={r})"
            
            if ratio < 1.0:
                return {
                    "metric_name": "min_ratio",
                    "metric_value": min_ratio,
                    "instances_tested": 2000 * len(sizes) * len(ensembles),
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
    
    return {
        "metric_name": "min_ratio",
        "metric_value": min_ratio,
        "instances_tested": 2000 * len(sizes) * len(ensembles),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")