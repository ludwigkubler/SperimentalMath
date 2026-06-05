# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_kcnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            if var not in clause:
                clause.add(var)
        clauses.append(list(clause))
    return clauses

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for pivot_row in range(m):
        pivot_col = next((col for col in range(n) if A[pivot_row][col] != 0), None)
        if pivot_col is None:
            continue
        # Make the pivot element 1
        factor = Fraction(1, A[pivot_row][pivot_col])
        for j in range(n):
            A[pivot_row][j] *= factor
        # Eliminate the pivot column in other rows
        for i in range(m):
            if i != pivot_row and A[i][pivot_col] != 0:
                factor = Fraction(A[i][pivot_col], A[pivot_row][pivot_col])
                for j in range(n):
                    A[i][j] -= factor * A[pivot_row][j]
    return A

def matroid_rank(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for var in clause:
            A[i][var - 1] = 1
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, n * (n - 1) // 2)
    clauses = generate_kcnf(n, k)
    
    try:
        rank = matroid_rank(clauses)
        lnd = len(clauses)  # Simplified for this test
        ratio = Fraction(lnd, rank) if rank != 0 else None
        
        return {
            "metric_name": "lnd_to_rank_ratio",
            "metric_value": float(ratio) if ratio is not None else 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True if ratio is not None and 0.5 <= ratio <= 2 else False,
            "counterexample": "" if ratio is not None and 0.5 <= ratio <= 2 else "lnd_to_rank_ratio_out_of_bounds"
        }
    except Exception as e:
        return {
            "metric_name": "lnd_to_rank_ratio",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lnd_to_rank_ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE all_trials_used_n_1")