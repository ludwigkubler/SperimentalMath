# auto-injected by SEC sandbox
import math
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import fractions
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def continued_fraction_expansion(x, K_trunc):
    cf = []
    for _ in range(K_trunc):
        x_inv = 1 / x
        q = int(x_inv)
        cf.append(q)
        x = x_inv - q
        if x == 0:
            break
    return cf

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

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def log2(x):
    return x.bit_length() - 1 if x > 0 else float('-inf')

def LZ77_phrase_count(T_f):
    n = len(T_f)
    LZ = 0
    i = 0
    while i < n:
        j = i + 1
        k = 0
        while j < n and T_f[j] == T_f[i]:
            j += 1
            k += 1
        if k > 0:
            LZ += 1
            i += k
        else:
            LZ += 2
            i += 1
    return LZ

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10]
    results = []
    for n in n_values:
        K_trunc = 4 * n
        families = ["uniform", "k-DNF_1", "k-DNF_n", "k-DNF_n^2", "dictator", "parity", "MAJORITY"]
        for family in families:
            if family == "uniform":
                T_f = [random.randint(0, 1) for _ in range(2**n)]
            elif family == "k-DNF_1":
                k = 1
                T_f = [random.choice([0, 1]) for _ in range(2**n)]
            elif family == "k-DNF_n":
                k = n
                T_f = [random.choice([0, 1]) for _ in range(2**n)]
            elif family == "k-DNF_n^2":
                k = n**2
                T_f = [random.choice([0, 1]) for _ in range(2**n)]
            elif family == "dictator":
                j = random.randint(0, n-1)
                T_f = [int(i == j) for i in range(n)] * (2**(n-1))
            elif family == "parity":
                T_f = [(sum(int(T_f[i]) for i in range(j+1)) % 2) for j in range(2**n)]
            elif family == "MAJORITY":
                threshold = n // 2
                T_f = [int(sum(int(T_f[i]) for i in range(n)) > threshold) for _ in range(2**n)]
            else:
                return {"metric_name": "", "metric_value": 0, "instances_tested": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
            
            r_f = sum(T_f[i] * 2**(-i-1) for i in range(2**n))
            cf_expansion = continued_fraction_expansion(r_f, K_trunc)
            freq_1 = sum(1 for a_i in cf_expansion if a_i == 1) / min(K_trunc, 4*n)
            GKD = abs(freq_1 - log2(4/3))
            LZ = LZ77_phrase_count(T_f)
            
            results.append({
                "metric_name": "GKD * log2(LZ + 2)",
                "metric_value": GKD * log2(LZ + 2),
                "instances_tested": 1,
                "conjecture_holds": GKD * log2(LZ + 2) <= 4 * sqrt(n),
                "counterexample": ""
            })
    
    total_metric = sum(result["metric_value"] for result in results)
    avg_metric = total_metric / len(results)
    std_metric = (sum((result["metric_value"] - avg_metric)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "GKD * log2(LZ + 2)",
        "metric_value": avg_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.95 and all(result["conjecture_holds"] for result in results) and max(result["metric_value"] for result in results) <= 1.2 * 4 * sqrt(n_values[-1]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = (sum((result["metric_value"] - avg_metric)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results) and max(result["metric_value"] for result in results) <= 1.2 * 4 * sqrt(n_values[-1]):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(result["metric_value"] > 1.2 * 4 * sqrt(n_values[-1]) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.2 * 4 * sqrt(n_values[-1]))
        print(f"RESULT: FALSIFIED counterexample=\"exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")