# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def minimal_index(T):
    n = len(T)
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        A[i][j] = Fraction(T[i][j], T[j][i])
    
    A = gaussian_elimination(A)
    min_idx = sum(1 for row in A if any(x != Fraction(0, 1) for x in row))
    return min_idx

def communication_complexity_rank(n):
    # Placeholder function; replace with actual computation
    return n * (n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        T = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
        min_idx = minimal_index(T)
        cc_rank = communication_complexity_rank(n)
        
        results.append({
            "n": n,
            "min_idx": min_idx,
            "cc_rank": cc_rank
        })
    
    if not results:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_idxs = [r["min_idx"] for r in results]
    cc_ranks = [r["cc_rank"] for r in results]
    
    mean_min_idx = sum(min_idxs) / len(min_idxs)
    mean_cc_rank = sum(cc_ranks) / len(cc_ranks)
    std_dev = math.sqrt(sum((x - mean_min_idx)**2 for x in min_idxs) / len(min_idxs))
    
    correlation_coefficient = sum((min_idxs[i] - mean_min_idx) * (cc_ranks[i] - mean_cc_rank) for i in range(len(min_idxs))) / (len(min_idxs) * std_dev * math.sqrt(sum((x - mean_cc_rank)**2 for x in cc_ranks)))
    
    return {
        "metric_name": "minimal_index",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and std_dev <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")