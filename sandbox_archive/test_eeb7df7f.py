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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = random.choice([0, 1])
            M[j][i] = M[i][j]
    return M

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def svd(A):
    m, n = len(A), len(A[0])
    U = [[0] * n for _ in range(m)]
    S = [0] * min(m, n)
    V = [[0] * m for _ in range(n)]
    
    # Compute A^T * A
    AT_A = matrix_multiplication(transpose(A), A)
    
    # Compute eigenvalues and eigenvectors of A^T * A
    eigenvals, eigenvecs = power_iteration(AT_A, n)
    
    # Sort eigenvalues and corresponding eigenvectors
    for i in range(n):
        S[i] = eigenvals[i]
        U[i] = [eigenvecs[j][i] for j in range(m)]
    
    # Compute V using A * U
    V = matrix_multiplication(A, U)
    
    return U, S, V

def transpose(M):
    m, n = len(M), len(M[0])
    T = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            T[j][i] = M[i][j]
    return T

def power_iteration(A, k):
    eigenvals = [1.0] * k
    eigenvecs = [[random.random() for _ in range(len(A))] for _ in range(k)]
    
    for _ in range(100):  # Number of iterations
        for i in range(k):
            v = matrix_multiplication(A, eigenvecs[i])
            norm = sum(x * x for x in v) ** 0.5
            eigenvals[i] = sum(v[j] * eigenvecs[j][i] for j in range(len(v)))
            eigenvecs[i] = [x / norm for x in v]
    
    return eigenvals, eigenvecs

def secant_rank(M):
    n = len(M)
    M_tensor = []
    for i in range(n):
        for j in range(n):
            M_tensor.append([M[i][k] * M[j][k] for k in range(n)])
    
    U, S, V = svd(M_tensor)
    rank = sum(1 for s in S if abs(s) > 1e-6)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_disjointness_matrix(n)
    
    sr_M = secant_rank(M)
    if sr_M < 0.8 * n:
        return {
            "metric_name": "secant rank",
            "metric_value": sr_M,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, sr(M)={sr_M}"
        }
    
    return {
        "metric_name": "secant rank",
        "metric_value": sr_M,
        "instances_tested": 1,
        "conjecture_holds": True,
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['instances_tested']}, sr(M)={results[0]['metric_value']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")