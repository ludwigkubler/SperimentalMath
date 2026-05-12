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
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def svd(M):
    m, n = len(M), len(M[0])
    U = [[0] * n for _ in range(m)]
    V = [[0] * n for _ in range(n)]
    S = [0] * n
    
    # Center the matrix
    mean = sum(sum(row) for row in M) / (m * n)
    M_centered = [[M[i][j] - mean for j in range(n)] for i in range(m)]
    
    # Compute U and V using power iteration
    for k in range(100):
        v = [random.gauss(0, 1) for _ in range(n)]
        v_norm = math.sqrt(sum(x**2 for x in v))
        v = [x / v_norm for x in v]
        
        u = [sum(M[i][j] * v[j] for j in range(n)) for i in range(m)]
        u_norm = math.sqrt(sum(x**2 for x in u))
        u = [x / u_norm for x in u]
        
        S[k] = sum(u[i] * M_centered[i][j] * v[j] for i in range(m) for j in range(n))
        
        for i in range(m):
            U[i][k] = u[i]
        
        for j in range(n):
            V[k][j] = v[j]
    
    return U, S, V

def max_singular_value(M):
    U, S, V = svd(M)
    return max(S)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    norm = max_singular_value(M)
    c = 0.5
    conjecture_holds = norm >= c * math.sqrt(n)
    counterexample = "" if conjecture_holds else "norm < c√n"
    
    return {
        "metric_name": "max_singular_value",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm < c√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")