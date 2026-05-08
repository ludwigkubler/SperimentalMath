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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def sparse_f2_gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    return A, b

def compute_betti_number(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if any(A[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def decision_tree_depth(f, n):
    memo = {}
    def dp(sigma):
        if sigma in memo:
            return memo[sigma]
        if all(s == '0' or s == '1' for s in sigma):
            return 0
        min_depth = float('inf')
        for i in range(n):
            new_sigma = sigma[:i] + '*' + sigma[i+1:]
            depth = dp(new_sigma)
            if depth < min_depth:
                min_depth = depth
        memo[sigma] = 1 + min_depth
        return memo[sigma]
    return dp('*' * n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8]
    results = []
    
    for n in n_values:
        for _ in range(30):
            f = [random.choice([0, 1]) for _ in range(2**n)]
            if all(f[i] == f[j] for i, j in zip(range(2**n), range(1, 2**n))):
                continue
            R_f = [(i, j) for i in range(2**n) for j in range(2**n) if f[i] != f[j]]
            W = set()
            for x, y in R_f:
                w = [j for j in range(n) if x & (1 << j) != y & (1 << j)]
                W.add(tuple(w))
            W_min = min(W, key=len)
            vertices = list(range(n))
            simplices = []
            for w in W_min:
                simplices.append([v for v in vertices if v not in w])
            beta_f = sum(2**len(simplex) - 1 for simplex in simplices)
            dt_depth = decision_tree_depth(f, n)
            results.append({
                "n": n,
                "f": f,
                "beta_f": beta_f,
                "dt_depth": dt_depth,
                "conjecture_holds": dt_depth >= math.ceil(math.log2(1 + beta_f))
            })
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    mean_beta = sum(result["beta_f"] for result in results) / len(results)
    std_beta = (sum((result["beta_f"] - mean_beta) ** 2 for result in results) / len(results)) ** 0.5
    
    return {
        "metric_name": "Betti Number",
        "metric_value": mean_beta,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.95 and all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_beta = sum(result["metric_value"] for result in results) / len(results)
    std_beta = (sum((result["metric_value"] - mean_beta) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.95 and all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_beta} std={std_beta} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if not result["conjecture_holds"])]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")