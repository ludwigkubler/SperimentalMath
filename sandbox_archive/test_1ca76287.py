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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        if all(A[i][j] == 0 for i in range(rank)):
            continue
        pivot_row = rank
        for i in range(pivot_row + 1, m):
            if A[i][j] != 0:
                A[pivot_row], A[i] = A[i], A[pivot_row]
                break
        for i in range(m):
            if i == pivot_row:
                continue
            factor = -A[i][j] / A[pivot_row][j]
            for k in range(n):
                A[i][k] += factor * A[pivot_row][k]
        rank += 1
    return rank

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for j in range(n):
        if all(A[i][j] == 0 for i in range(m)):
            continue
        pivot_row = max(range(j, m), key=lambda i: abs(A[i][j]))
        A[j], A[pivot_row] = A[pivot_row], A[j]
        for i in range(m):
            if i == j:
                continue
            factor = -A[i][j] / A[j][j]
            for k in range(n):
                A[i][k] += factor * A[j][k]
    return A

def generate_protocol(seed, n):
    random.seed(seed)
    protocol = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return protocol

def lie_algebroid_cohomology_rank(protocol):
    m = len(protocol)
    A = [[sum(row[i] * col[j] for row in protocol) for j in range(m)] for i in range(m)]
    rank = matrix_rank(A)
    return rank

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        protocol = generate_protocol(seed, n)
        cohomology_rank = lie_algebroid_cohomology_rank(protocol)
        rank_variance = sum((protocol[i][j] - (sum(row[j] for row in protocol) / n))**2 for i in range(n) for j in range(n)) / (n * n)
        results.append({
            "n": n,
            "cohomology_rank": cohomology_rank,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "cohomology_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cohomology_ranks = [r["cohomology_rank"] for r in results]
    rank_variances = [r["rank_variance"] for r in results]
    mean_cohomology_rank = sum(cohomology_ranks) / len(cohomology_ranks)
    std_deviation = math.sqrt(sum((x - mean_cohomology_rank)**2 for x in cohomology_ranks) / len(cohomology_ranks))
    
    conjecture_holds = all(r["cohomology_rank"] <= r["rank_variance"]**0.5 for r in results)
    counterexample = "" if conjecture_holds else "counterexample_found"
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": mean_cohomology_rank,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_deviation:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"counterexample_found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")