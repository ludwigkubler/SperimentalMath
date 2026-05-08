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
        max_row = i + max(range(i, n), key=lambda x: abs(A[x][i]))
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

def spectral_norm(M):
    n = len(M)
    v = [1] * n
    for _ in range(100):  # Power iteration method
        v = matrix_multiply(M, v)
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    return max(abs(v[i]) for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    size_P = 2**n
    
    # Construct transition matrix M_P for a read-twice BP
    M_P = [[0] * size_P for _ in range(size_P)]
    for i in range(n):
        for j in range(1 << i):
            for k in range(1 << (n - i - 1)):
                M_P[j + (k << (i + 1))][j | k] += 1
                M_P[j + (k << (i + 1))][j & ~k] += 1
    
    # Compute spectral norm of M_P
    norm_M_P = spectral_norm(M_P)
    
    # Construct transition matrix for IP_2 function
    M_IP2 = [[0] * size_P for _ in range(size_P)]
    for i in range(n):
        for j in range(1 << i):
            for k in range(1 << (n - i - 1)):
                M_IP2[j + (k << (i + 1))][j | k] += 1
                M_IP2[j + (k << (i + 1))][j & ~k] += 1
    
    # Compute spectral norm of IP_2 matrix
    norm_IP2 = spectral_norm(M_IP2)
    
    return {
        "metric_name": "spectral_norm",
        "metric_value": norm_M_P,
        "instances_tested": n,
        "conjecture_holds": norm_IP2 > 10 * math.log(size_P),
        "counterexample": "" if norm_IP2 > 10 * math.log(size_P) else f"IP_2 function with size {size_P} has norm {norm_IP2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 function norm is smaller than expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")