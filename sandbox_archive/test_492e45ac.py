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

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def euler_characteristic(R, n):
    chi = 0
    for d in range(n + 1):
        sign = (-1) ** d
        C_n_d = binomial(n, d)
        sum_w0 = 0
        for w0 in R:
            if w0 >= d and all(w0 - i not in R for i in range(1, d + 1)):
                sum_w0 += binomial(n - d, w0)
        chi += sign * C_n_d * sum_w0
    return chi

def dnf_min(f):
    n = len(f)
    minterms = []
    for i in range(2 ** n):
        if f[i]:
            minterms.append([i & (1 << j) > 0 for j in range(n)])
    
    prime_implicants = []
    covered = [False] * len(minterms)
    for i in range(len(minterms)):
        if not covered[i]:
            pi = minterms[i]
            covered[i] = True
            for j in range(i + 1, len(minterms)):
                if all(pi[k] or minterms[j][k] for k in range(n)) and not covered[j]:
                    covered[j] = True
            prime_implicants.append(pi)
    
    return len(prime_implicants)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8, 10]
    results = []
    for n in n_values:
        R_f = set()
        if n <= 7:
            R_f = {random.randint(0, n) for _ in range(30)}
        else:
            R_f = {random.randint(0, n) for _ in range(30)}
        
        f = [False] * (2 ** n)
        for k in R_f:
            for i in range(k + 1):
                for comb in itertools.combinations(range(n), i):
                    idx = sum(1 << j for j in comb)
                    f[idx] = True
        
        chi_K_f = euler_characteristic(R_f, n)
        dnf_min_f = dnf_min(f)
        
        results.append({
            "n": n,
            "R_f": R_f,
            "chi_K_f": chi_K_f,
            "dnf_min_f": dnf_min_f,
            "ratio": abs(chi_K_f) / dnf_min_f if dnf_min_f != 0 else float('inf')
        })
    
    metric_value = sum(abs(r["chi_K_f"]) for r in results)
    instances_tested = len(results)
    conjecture_holds = all(abs(r["chi_K_f"]) <= r["dnf_min_f"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Euler Characteristic vs DNF-Min",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")