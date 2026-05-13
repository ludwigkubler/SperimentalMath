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
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if abs(A[i_max][j]) < 1e-9:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def tensor_product(a, b):
    m, n = len(a), len(a[0])
    p, q = len(b), len(b[0])
    result = [[0 for _ in range(q)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j+k] += a[i][j] * b[k][j]
    return result

def generate_disjointness_matrix(n):
    M = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if (i & j) == 0:
                M[i][j] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M_n = generate_disjointness_matrix(n)
        rank = gaussian_elimination(M_n)
        if rank != n:
            return {
                "metric_name": "rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Disjointness matrix M_{n} has rank {rank}, expected {n}"
            }
        results.append(rank)
    
    return {
        "metric_name": "rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r == n_values[0]) / len(n_values)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r != n_values[0])]
        print(f"RESULT: FALSIFIED counterexample='disjointness_matrix_rank' first_failing_seed={first_failing_seed}")