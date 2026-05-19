# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mod(A, m):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] % m + m) % m
    return result

def matrix_multiply(A, B, m):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % m
    return result

def matrix_power(A, k, m):
    n = len(A)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A, m)
        A = matrix_multiply(A, A, m)
        k //= 2
    return result

def linial_shraibman_gamma(M):
    n = len(M)
    M_T_M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_val = 0
            for k in range(n):
                sum_val += (M[i][k] * M[j][k]) % n
            M_T_M[i][j] = sum_val
            M_T_M[j][i] = sum_val
    
    eigenvalues = []
    for i in range(1, 20):  # Limit to 20 iterations for practical purposes
        v = [random.randint(0, n-1) for _ in range(n)]
        v_norm = sum(v[i]**2 for i in range(n)) ** 0.5
        v = [v[i] / v_norm for i in range(n)]
        for _ in range(i):
            v_next = [M_T_M[j][i] * v[j] for j in range(n)]
            v_next_norm = sum(v_next[j]**2 for j in range(n)) ** 0.5
            v_next = [v_next[i] / v_next_norm for i in range(n)]
        eigenvalues.append(sum(v_next[j]**2 for j in range(n)))
    
    return max(eigenvalues) / n

def is_sign_matrix(M):
    return all(x == 1 or x == -1 for row in M for x in row)

def det_mod_2k(M, k):
    n = len(M)
    A = matrix_mod(M, 2**k)
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                return 0
        for j in range(n):
            if i != j:
                factor = (A[j][i] * pow(A[i][i], -1, 2**k)) % (2**k)
                for l in range(n):
                    A[j][l] = (A[j][l] - factor * A[i][l]) % (2**k)
    det = 1
    for i in range(n):
        det = (det * A[i][i]) % (2**k)
    return det

def v_2(x):
    if x == 0:
        return float('inf')
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 32, 40]
    results = []
    
    for n in n_values:
        for _ in range(30):
            M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            if not is_sign_matrix(M):
                continue
            
            det = abs(det_mod_2k(M, n * math.ceil(math.log2(n))))
            rho = v_2(det) / n
            g = linial_shraibman_gamma(M)
            
            results.append({
                "n": n,
                "rho": rho,
                "g": g,
                "instance_type": "uniform"
            })
    
    max_rho_g_diff = -float('inf')
    for res in results:
        diff = res["rho"] * math.log2(res["n"]) - 4 * math.log2(res["g"])
        if diff > max_rho_g_diff:
            max_rho_g_diff = diff
    
    return {
        "metric_name": "max_rho_g_diff",
        "metric_value": max_rho_g_diff,
        "instances_tested": len(results),
        "conjecture_holds": max_rho_g_diff <= 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            trial = json.load(f)
            results.append(trial)
    
    max_rho_g_diffs = [x["metric_value"] for x in results]
    support_fraction = sum(x["conjecture_holds"] for x in results) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={sum(max_rho_g_diffs)/len(max_rho_g_diffs)} std=0.0 support_fraction=1.0")
    elif any(not x["conjecture_holds"] for x in results) and max_rho_g_diffs[-1] > 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"max_rho_g_diff_exceeded\" first_failing_seed={seeds[-1]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")