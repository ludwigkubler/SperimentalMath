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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    return M

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def svd(A):
    m, n = len(A), len(A[0])
    U = [[0] * m for _ in range(m)]
    V = [[0] * n for _ in range(n)]
    S = [0] * min(m, n)
    
    # Center the matrix
    A_centered = [[A[i][j] - (sum(A[i]) / n) * (sum(row[j] for row in A) / m) for j in range(n)] for i in range(m)]
    
    # Compute SVD using power iteration method
    for _ in range(100):
        u = [random.random() for _ in range(m)]
        v = [random.random() for _ in range(n)]
        
        u = [x / math.sqrt(sum(x**2 for x in u)) for x in u]
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
        
        A_u = matrix_multiplication(A, u)
        sigma = sum(A_u[i] * v[i] for i in range(n))
        u = [A_u[i] - sigma * v[i] for i in range(m)]
        u = [x / math.sqrt(sum(x**2 for x in u)) for x in u]
        
        A_vT = matrix_multiplication(A, v)
        sigma = sum(A_vT[j] * u[j] for j in range(m))
        v = [A_vT[j] - sigma * u[j] for j in range(n)]
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
        
        S[0] += sigma ** 2
    
    return U, S, V

def secant_rank(M):
    M_tensor = matrix_multiplication(M, M)
    _, S, _ = svd(M_tensor)
    rank = sum(1 for s in S if abs(s) > 1e-6)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        M = generate_disjointness_matrix(n)
        sr_M = secant_rank(M)
        
        if sr_M < 0.8 * n:
            return {
                "metric_name": "secant_rank",
                "metric_value": sr_M,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, sr(M)={sr_M}"
            }
        
        total_metric_value += sr_M
        instances_tested += 1
    
    return {
        "metric_name": "secant_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")