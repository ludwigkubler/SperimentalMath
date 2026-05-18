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
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
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

def vector_norm(v):
    return math.sqrt(sum(x**2 for x in v))

def frobenius_norm(A):
    return sum(vector_norm(row) ** 2 for row in A)

def largest_singular_value(M):
    m, n = len(M), len(M[0])
    U, S, Vt = [], [], []
    gaussian_elimination(M)
    for i in range(min(m, n)):
        u = [M[j][i] / M[i][i] if j == i else 0 for j in range(m)]
        s = math.sqrt(sum(x**2 for x in u))
        U.append([x / s for x in u])
        S.append(s)
    return max(S)

def vec(M):
    return [x for row in M for x in row]

def layer_difference_stack(T0, T1):
    return [vec(T1[i] - T0[i]) for i in range(len(T0))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(3, 9)
    w = random.choice([3, 4, 5, 6])
    L = 4 * n
    s = w * L
    
    # Generate random RT-BP
    T0 = [[[random.randint(0, 1) for _ in range(w)] for _ in range(w)] for _ in range(L)]
    T1 = [[[random.randint(0, 1) for _ in range(w)] for _ in range(w)] for _ in range(L)]
    
    D = layer_difference_stack(T0, T1)
    norm_F = frobenius_norm(D)
    norm_op = largest_singular_value(D)
    
    if norm_F == 0 and norm_op == 0:
        rho = 0
    else:
        rho = math.log2(norm_F**2 / norm_op**2)
    
    # Check upper bound for random RT-BP
    if rho > 2 * math.log2(s + 1):
        return {
            "metric_name": "rho",
            "metric_value": rho,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Random RT-BP failed upper bound with rho={rho}"
        }
    
    # Construct canonical exponential-width RT-BP for IP_2
    if n <= 9:
        IP2 = [[[0] * (2**(n+1)) for _ in range(2**(n+1))] for _ in range(w)]
        for i in range(n):
            for j in range(2**i, 2**(i+1)):
                for k in range(2**i, 2**(i+1)):
                    IP2[j][k][j ^ k] = 1
        D_IP2 = layer_difference_stack(IP2, [[IP2[i][j][k] for j in range(w)] for i in range(L)])
        norm_F_IP2 = frobenius_norm(D_IP2)
        norm_op_IP2 = largest_singular_value(D_IP2)
        
        if norm_F_IP2 == 0 and norm_op_IP2 == 0:
            rho_IP2 = 0
        else:
            rho_IP2 = math.log2(norm_F_IP2**2 / norm_op_IP2**2)
        
        # Check lower bound for canonical IP_2 RT-BP
        if rho_IP2 < n / 4:
            return {
                "metric_name": "rho",
                "metric_value": rho_IP2,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Canonical IP_2 RT-BP failed lower bound with rho={rho_IP2}"
            }
    
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    rho_values = [r["metric_value"] for r in results if "rho" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(rho_values)/len(rho_values)} std={math.sqrt(sum((x - sum(rho_values)/len(rho_values))**2 for x in rho_values) / len(rho_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")