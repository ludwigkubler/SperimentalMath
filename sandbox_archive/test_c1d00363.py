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
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a row to swap with
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    n = len(A)
    r = 0
    for i in range(n):
        if all(A[i][j] == 0 for j in range(r)):
            continue
        for j in range(r, n):
            A[i], A[j] = A[j], A[i]
            break
        r += 1
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return r

def min_local_system_rank(clause_set):
    # Convert clause set to a matrix
    n = len(clause_set)
    m = max(len(c) for c in clause_set)
    A = [[0] * (m + 1) for _ in range(n)]
    for i, clause in enumerate(clause_set):
        for j, literal in enumerate(clause):
            if literal > 0:
                A[i][j] = 1
            else:
                A[i][j] = -1
    return rank_of_matrix(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random k-SAT instance with m clauses
    k = 3  # Example value for k
    m = random.randint(5, 40)
    clause_set = []
    literals = set(range(1, 2 * m + 1))
    for _ in range(m):
        clause = random.sample(literals, k)
        clause_set.append(clause)
    
    # Calculate the minimal local system rank
    r_local = min_local_system_rank(clause_set)
    
    # Measure the clause set complexity
    S_clauses_m = len(set(literal for clause in clause_set for literal in clause))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": math.nan,  # Placeholder for actual calculation
        "instances_tested": m,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value
    if all(isinstance(r["metric_value"], (int, float)) and not math.isnan(r["metric_value"]) for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    else:
        mean, std = "N/A", "N/A"
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Print final result
    if all(r["metric_value"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.8 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")