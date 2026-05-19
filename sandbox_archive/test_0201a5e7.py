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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def kronecker_product(A, B):
    n = len(A)
    m = len(B)
    p = len(A[0])
    q = len(B[0])
    C = [[0] * (m*q) for _ in range(n*p)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                for l in range(q):
                    C[i*m + j][k*q + l] = A[i][k] * B[j][l]
    return C

def build_read_twice_bp(n):
    w = 2**n
    T_p_b = [[random.randint(0, 1) for _ in range(w)] for _ in range(4*n)]
    D_p = [T_p_1 - T_p_0 for T_p_1, T_p_0 in zip(T_p_b[::2], T_p_b[1::2])]
    K_P = sum(kronecker_product(D_p[i], D_p[j]) for i in range(n) for j in range(i+1, n))
    return K_P

def compute_rho(n):
    w = 2**n
    P_IP2 = build_read_twice_bp(n)
    P_rand = [[random.randint(0, 1) for _ in range(w)] for _ in range(4*n)]
    D_p_ip2 = [T_p_1 - T_p_0 for T_p_1, T_p_0 in zip(P_IP2[::2], P_IP2[1::2])]
    K_P_ip2 = sum(kronecker_product(D_p_ip2[i], D_p_ip2[j]) for i in range(n) for j in range(i+1, n))
    
    rho_ip2 = gaussian_elimination(K_P_ip2)
    rho_rand = gaussian_elimination(P_rand)
    
    return len(rho_ip2), len(rho_rand)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [2, 3, 4, 5]
    rho_ip2_total = 0
    rho_rand_total = 0
    
    for n in n_values:
        rho_ip2, rho_rand = compute_rho(n)
        rho_ip2_total += rho_ip2
        rho_rand_total += rho_rand
    
    mean_rho_ip2 = rho_ip2_total / (4 * len(n_values))
    mean_rho_rand = rho_rand_total / (4 * len(n_values))
    
    if mean_rho_ip2 < 2**n_values[0]/4:
        return {
            "metric_name": "rho(P)",
            "metric_value": mean_rho_ip2,
            "instances_tested": 4 * len(n_values),
            "conjecture_holds": False,
            "counterexample": f"rho(P_IP2) < 2^{n_values[0]}/4"
        }
    
    support_fraction = rho_ip2_total / (len(n_values) * 4)
    return {
        "metric_name": "rho(P)",
        "metric_value": mean_rho_ip2,
        "instances_tested": 4 * len(n_values),
        "conjecture_holds": support_fraction >= 0.75 and rho_ip2_total / rho_rand_total >= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_rho_ip2 = sum(r["metric_value"] for r in results) / len(results)
    std_rho_ip2 = math.sqrt(sum((r["metric_value"] - mean_rho_ip2)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_ip2} std={std_rho_ip2} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_rho_ip2} std={std_rho_ip2} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho(P_IP2) < 2^{n_values[0]}/4\" first_failing_seed={first_failing_seed}")