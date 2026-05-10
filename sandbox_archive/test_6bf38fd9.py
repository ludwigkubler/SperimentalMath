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
    M_scaled = [[M[i][j] ** (1/p) for j in range(n)] for i in range(n)]
    norm = math.sqrt(sum(sum(row[j]**2 for row in M_scaled) for j in range(n)))
    return norm

def generate_product_support_matrix(n):
    S = [random.randint(0, n-1) for _ in range(n)]
    T = [random.randint(0, n-1) for _ in range(n)]
    M = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if S[i] == T[j]:
                M[i][j] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    p = 1.5
    threshold = 0.1 * math.sqrt(n)
    
    M = generate_product_support_matrix(n)
    norm = noncommutative_lp_norm(M, p)
    
    metric_name = "noncommutative_Lp_norm"
    metric_value = norm
    instances_tested = 1
    conjecture_holds = norm >= threshold
    counterexample = "" if conjecture_holds else f"norm={norm} < {threshold}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm < threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")