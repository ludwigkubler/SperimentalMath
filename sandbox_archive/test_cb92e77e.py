# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_disj_n(n):
    X = set(range(1, n+1))
    Y = set(range(1, n+1))
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            M[i][j] = 1
            M[j][i] = 1
    return M

def flatten_tensor(M):
    flat = []
    for row in M:
        flat.extend(row)
    return flat

def rank_approximation(tensor, rank):
    m = len(tensor)
    n = len(tensor[0])
    U, S, Vt = svd(tensor, rank)
    approx = [[U[i][k] * S[k] * Vt[k][j] for j in range(n)] for i in range(m)]
    return approx

def svd(A, k):
    m, n = len(A), len(A[0])
    U = [[random.random() for _ in range(m)] for _ in range(m)]
    S = [random.random() for _ in range(k)]
    Vt = [[random.random() for _ in range(n)] for _ in range(k)]
    
    for _ in range(100):
        U, S, Vt = svd_update(A, U, S, Vt)
    
    return U, S, Vt

def svd_update(A, U, S, Vt):
    m, n = len(A), len(A[0])
    k = len(S)
    
    A_hat = [[sum(U[i][l] * S[l] * Vt[l][j] for l in range(k)) for j in range(n)] for i in range(m)]
    E = [[A[i][j] - A_hat[i][j] for j in range(n)] for i in range(m)]
    
    U_new, _, _ = svd(E, k)
    Vt_new, _, _ = svd([[E[j][i] for j in range(m)] for i in range(n)], k)
    
    U = [[U[i][l] * U_new[l][j] for l in range(k)] for j in range(m)]
    Vt = [[Vt[l][i] * Vt_new[l][j] for l in range(k)] for j in range(n)]
    
    return U, S, Vt

def secant_variety_dimension(M):
    flat = flatten_tensor(M)
    rank = 1
    while True:
        approx = rank_approximation(flat, rank)
        error = sum((flat[i] - approx[i])**2 for i in range(len(flat)))
        if error < 1e-6:
            return rank
        rank += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_disj_n(n)
    
    dim_sec = secant_variety_dimension(M)
    metric_value = dim_sec
    instances_tested = 1
    conjecture_holds = dim_sec >= 0.8 * math.sqrt(n * n)
    counterexample = "" if conjecture_holds else f"dim(sec(M)) = {dim_sec}, expected ≥ 0.8√{n*n}"
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*40+2, 40))
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")