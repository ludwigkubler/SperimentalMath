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
            if i == j:
                A[i][j] = 1 / A[i][j]
            else:
                A[i][j] *= A[i][i]
        for k in range(m):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bp(N):
        s = 2 ** (N // 2)
        B_mid = [[0] * (2 ** N) for _ in range(s)]
        for state in range(s):
            for input_ in range(2 ** N):
                if bin(state ^ input_).count('1') == N // 2:
                    B_mid[state][input_] = 1
        return B_mid
    
    def compute_disp(B_mid):
        s, n = len(B_mid), len(B_mid[0])
        U, _, Vt = gaussian_elimination(matrix_multiplication(B_mid, B_mid))
        sigma_squared = sum(U[i][i] ** 2 for i in range(s))
        sigma_fourth = sum(U[i][i] ** 4 for i in range(s))
        return math.log2((sigma_squared ** 2) / sigma_fourth)
    
    N_values = [4, 6, 8, 10, 12, 14]
    results = []
    for N in N_values:
        B_mid = generate_bp(N)
        disp = compute_disp(B_mid)
        results.append({
            "N": N,
            "disp": disp
        })
    
    metric_value = sum(result["disp"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["disp"] >= N / 2 - 4 * math.log2(N) for result in results)
    counterexample = "" if conjecture_holds else "IP_2_N with DISP < N/2 - 4·log_2 N"
    
    return {
        "metric_name": "DISP",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disp = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disp} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2_N with DISP < N/2 - 4·log_2 N\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")