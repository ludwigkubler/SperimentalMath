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
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    # Back substitution
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A[i][-1], A[i][i])
        for k in range(i-1, -1, -1):
            A[k][-1] -= A[k][i] * x[i]

    return [x[i] for i in range(n)]

def minimal_rank(F):
    n = len(F)
    A = [[F[i][j] - F[i][k] * F[k][j] for j in range(n)] for k in range(1, n)]
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    F = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if M[i][j]:
                F[i][j] = 1
    
    min_rank_F = minimal_rank(F)
    expected_min_rank = math.log2(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_F,
        "instances_tested": n * n,
        "conjecture_holds": abs(min_rank_F - expected_min_rank) <= 0.5 * expected_min_rank,
        "counterexample": "" if conjecture_holds else f"n={n}, M={M}, F={F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")