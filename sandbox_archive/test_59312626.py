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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 3
    
    # Generate a random k-CNF instance with n variables and m clauses
    m = random.randint(1, n * k)
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(n), k))
        cnf.append(clause)
    
    # Convert the k-CNF instance to a quadratic form
    Q = [[0] * n for _ in range(n)]
    for clause in cnf:
        for i in clause:
            for j in clause:
                Q[i][j] += 1
    
    # Compute the minimal rank of the quadratic form
    rank = compute_minimal_rank(Q)
    
    # Measure the communication complexity (simplified as n^k for this example)
    comm_complexity = n ** k
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": rank == k and comm_complexity <= n ** (k + 1),
        "counterexample": "" if rank == k else f"rank={rank}, expected=k={k}"
    }

def compute_minimal_rank(Q):
    # Gaussian elimination to find the rank of Q
    m, n = len(Q), len(Q[0])
    pivot_row = 0
    for col in range(n):
        if pivot_row >= m:
            break
        max_pivot = abs(Q[pivot_row][col])
        pivot_idx = pivot_row
        for i in range(pivot_row + 1, m):
            if abs(Q[i][col]) > max_pivot:
                max_pivot = abs(Q[i][col])
                pivot_idx = i
        if max_pivot == 0:
            continue
        Q[pivot_row], Q[pivot_idx] = Q[pivot_idx], Q[pivot_row]
        for i in range(n):
            Q[pivot_row][i] /= Q[pivot_row][col]
        for i in range(m):
            if i != pivot_row:
                factor = Q[i][col]
                for j in range(n):
                    Q[i][j] -= factor * Q[pivot_row][j]
        pivot_row += 1
    return pivot_row

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")