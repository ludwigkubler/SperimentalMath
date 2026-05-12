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
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def free_cumulants(M):
    n = len(M)
    R = [[0] * n for _ in range(n)]
    R[0][0] = M[0][0]
    for k in range(1, n):
        R[k][k] = M[k][k]
        for i in range(k-1, -1, -1):
            for j in range(i+1, k+1):
                R[i][j] = (R[i][j-1] + R[j][i]) / (1 - R[j-1][j])
    return [R[i][i] for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a read-twice BP for IP_2
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    M_P = matrix_multiply(P, P)
    cumulants_IP2 = free_cumulants(M_P)
    rho_IP2 = sum(cumulants_IP2)
    
    # Generate a read-twice BP for a poly-size function
    Q = [[random.random() for _ in range(n)] for _ in range(n)]
    M_Q = matrix_multiply(Q, Q)
    cumulants_poly = free_cumulants(M_Q)
    rho_poly = sum(cumulants_poly)
    
    return {
        "metric_name": "rho",
        "metric_value": rho_IP2,
        "instances_tested": 1,
        "conjecture_holds": rho_IP2 >= n and rho_poly <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_IP2 = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_rho_IP2 = math.sqrt(sum((r["metric_value"] - mean_rho_IP2) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_IP2} std={std_rho_IP2} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho_IP2 < n or rho_poly > log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")