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
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        for r in range(i+1, n):
            factor = A[r][i] / pivot
            for c in range(i, n):
                A[r][c] -= factor * A[i][c]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def minimal_rank(F):
    n = len(F)
    A = [[F[i][j] - F[i][k] * F[k][j] for j in range(n)] for k in range(1, n)]
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Convert M to a quadratic form F
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if M[i][j]:
                F[i][j] = 1
    
    min_rank_F = minimal_rank(F)
    
    # Calculate the expected rank (Θ(log n))
    expected_rank = math.log2(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_F,
        "instances_tested": 1,
        "conjecture_holds": abs(min_rank_F - expected_rank) <= 2 * expected_rank,
        "counterexample": "" if conjecture_holds else f"min_rank_F={min_rank_F}, expected_rank={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")