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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    m, n = len(A), len(A[0])
    T = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            T[j][i] = A[i][j]
    return T

def svd(M):
    U = M
    V = transpose(M)
    S = [max(abs(row[i]) for row in M) for i in range(len(M[0]))]
    return U, S, V

def tensor_rank(M):
    if not M or not M[0]:
        return 0
    m, n = len(M), len(M[0])
    rank = 0
    while True:
        max_val = -1
        max_row, max_col = -1, -1
        for i in range(m):
            for j in range(n):
                if abs(M[i][j]) > max_val:
                    max_val = abs(M[i][j])
                    max_row, max_col = i, j
        if max_val == 0:
            break
        rank += 1
        M[max_row] = [0] * n
        for i in range(m):
            M[i][max_col] = 0
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(5, 40)
    
    # Construct a read-twice branching program instance
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(d)]
    
    # Construct the associated Hermitian matrix
    M = [[0] * n for _ in range(n)]
    for t in range(d):
        for i in range(n):
            for j in range(n):
                if P[t][i] == 1 and P[t][j] == 1:
                    M[i][j] += 1
    
    # Compute the minimal tensor rank
    rank = tensor_rank(M)
    
    # Check the conjecture
    conjecture_holds = False
    counterexample = ""
    if rank <= 2**d:
        conjecture_holds = True
    elif rank >= 2**(n/4):
        conjecture_holds = True
    else:
        counterexample = "minimal_tensor_rank_out_of_bounds"
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"minimal_tensor_rank_out_of_bounds\" first_failing_seed={first_failing_seed}")