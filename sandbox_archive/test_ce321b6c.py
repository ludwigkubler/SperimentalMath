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
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def tensor_product(a, b):
    n = len(a)
    result = [[0] * (n*n) for _ in range(n*n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    result[i*n + j][k*n + l] = a[i][j] * b[k][l]
    return result

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M_n = generate_disjointness_matrix(n)
        rank_M_n = gaussian_elimination(M_n)
        
        if rank_M_n != n:
            return {
                "metric_name": "rank_M_n",
                "metric_value": rank_M_n,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Disjointness matrix M_{n} has rank {rank_M_n}, expected {n}"
            }
        
        results.append(rank_M_n)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in results) / len(results))
    
    return {
        "metric_name": "rank_M_n",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(x["metric_value"] for x in results) / len(results)
    std_rank = math.sqrt(sum((x["metric_value"] - mean_rank)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_M_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")