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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        rank += 1
        for i in range(rank, m):
            factor = A[i][j] / A[pivot_row][j]
            for k in range(n):
                A[i][k] -= factor * A[pivot_row][k]
    return rank

def min_rank(M):
    n = len(M)
    M_copy = [row[:] for row in M]
    rank = gaussian_elimination(M_copy)
    return rank

def communication_complexity_disjointness(M):
    n = len(M)
    max_distance = 0
    for i in range(n):
        for j in range(i + 1, n):
            distance = sum(1 for x, y in zip(M[i], M[j]) if x != y)
            max_distance = max(max_distance, distance)
    return max_distance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    N = n
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    δ = communication_complexity_disjointness(M)
    if δ >= math.log(N / 0.5):
        return {
            "metric_name": "min_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    rank = min_rank(M)
    c = 0.5
    if rank >= c * math.log(n / δ):
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank {rank} < {c * math.log(n / δ)} with δ = {δ}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")