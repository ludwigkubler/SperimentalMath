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

def lu_decomposition(A):
    n = len(A)
    L = [[0 for _ in range(n)] for _ in range(n)]
    U = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            sum_upper = sum(L[k][j] * U[k][i] for k in range(i))
            U[i][j] = A[i][j] - sum_upper
        for j in range(i+1, n):
            sum_lower = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - sum_lower) / U[i][i]
    return L, U

def tensor_rank(A):
    _, U = lu_decomposition(A)
    rank = sum(1 for u in U if abs(u[-1]) > 1e-9)
    return rank

def secant_variety_dimension(rank):
    return rank**2 - rank + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    X = set(range(n))
    Y = set(range(n))
    M = [[int(x != y) for x in X] for y in Y]
    
    rank = tensor_rank(M)
    dim_secant = secant_variety_dimension(rank)
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": dim_secant,
        "instances_tested": 1,
        "conjecture_holds": dim_secant >= n / 2,
        "counterexample": "" if dim_secant >= n / 2 else f"Rank-2 tensor decomposition has dimension {dim_secant}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank-2 tensor decomposition has dimension less than n/2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")