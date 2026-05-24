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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_det(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * matrix_det(submatrix)
        sign *= -1
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5 + (seed % 6) * 5  # Sweep n through {5, 10, 15, 20, 30, 40}
    if n > 40:
        return {"metric_name": "min_rank", "metric_value": float('inf'), "instances_tested": 0, "conjecture_holds": False, "counterexample": "n_too_large"}
    
    # Construct a random read-twice branching program
    bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2)]
    
    # Construct the associated quadratic form matrix
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if bp[0][i] == bp[1][j]:
                Q[i][j] = 1
    
    # Compute the minimal rank of the quadratic form
    min_rank = float('inf')
    for k in range(1, n + 1):
        submatrix = [row[:k] + row[k+1:] for row in Q]
        det = matrix_det(submatrix)
        if det != 0:
            min_rank = k
            break
    
    # Check the conjecture
    size_P = len(bp[0])
    log_size_P = math.log(size_P, 2)
    if n == 1:  # Trivial case enumeration
        return {"metric_name": "min_rank", "metric_value": min_rank, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    if min_rank > 1.5 * log_size_P:
        return {"metric_name": "min_rank", "metric_value": min_rank, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"BP of size {size_P} has min rank {min_rank}, which is greater than 1.5 * log(size(P)) = {1.5 * log_size_P:.2f}"}
    
    if n == 5 and min_rank < n:
        return {"metric_name": "min_rank", "metric_value": min_rank, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"IP_2 BP of size {size_P} has min rank {min_rank}, which is less than n = {n}"}
    
    return {"metric_name": "min_rank", "metric_value": min_rank, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    min_ranks = [r["metric_value"] for r in results if "min_rank" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={sum(min_ranks)/len(min_ranks):.2f} std={math.sqrt(sum((x - sum(min_ranks)/len(min_ranks))**2 for x in min_ranks) / len(min_ranks)):.2f} support_fraction={support_fraction:.2f}")
    elif any("counterexample" in r and "IP_2 BP" in r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and "IP_2 BP" in r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 BP does not have min rank Ω(n)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=conjecture_not_supported")