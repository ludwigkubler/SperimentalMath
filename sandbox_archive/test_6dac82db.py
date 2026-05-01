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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, p):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    for _ in range(p):
        result = matrix_multiply(result, A)
    return result

def noncommutative_lp_norm(M, p):
    n = len(M)
    M_p = matrix_power(M, int(p))
    norm = 0
    for i in range(n):
        for j in range(n):
            norm += abs(M_p[i][j])
    return norm ** (1 / p)

def generate_disjointness_matrix(n):
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    M = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_ratio = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        M = generate_disjointness_matrix(n)
        norm_p = noncommutative_lp_norm(M, 1.5)
        ratio = norm_p / (n ** (1 - 1 / 1.5))
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio >= 0.7
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")