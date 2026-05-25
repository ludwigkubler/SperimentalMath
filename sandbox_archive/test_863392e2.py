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

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rref = [row[:] for row in A]
    lead = 0
    for r in range(m):
        if lead >= n:
            break
        i = r
        while i < m and rref[i][lead] == 0:
            i += 1
        if i != r:
            rref[r], rref[i] = rref[i], rref[r]
        pivot = rref[r][lead]
        for j in range(n):
            rref[r][j] /= pivot
        for i in range(m):
            if i != r and rref[i][lead]:
                factor = rref[i][lead]
                for j in range(n):
                    rref[i][j] -= factor * rref[r][j]
        lead += 1
    return rref

def rank(A):
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(row))
    return rank

def algebraic_stack_rank(n, m):
    # Construct the clause indicator matrix
    A = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if random.choice([True, False]):
                A[i][j] = 1
    
    return rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        m = n * 2  # Example ratio of clauses to variables
        rank_value = algebraic_stack_rank(n, m)
        bound = m ** 0.5 * n ** 0.25
        
        results.append({
            "n": n,
            "m": m,
            "rank_value": rank_value,
            "bound": bound
        })
    
    mean_rank = sum(result["rank_value"] for result in results) / len(results)
    max_bound = max(result["bound"] for result in results)
    
    conjecture_holds = all(result["rank_value"] <= result["bound"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "algebraic_stack_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")