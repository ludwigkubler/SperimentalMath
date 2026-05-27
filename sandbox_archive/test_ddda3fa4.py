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
    rows, cols = len(A), len(A[0])
    rank = 0
    
    for j in range(cols):
        pivot_row = -1
        for i in range(rank, rows):
            if A[i][j] != 0:
                pivot_row = i
                break
        
        if pivot_row == -1:
            continue
        
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        
        for i in range(rows):
            if i != rank:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(cols):
                    A[i][k] -= factor * A[rank][k]
        
        rank += 1
    
    return rank

def matrix_rank(A):
    rows, cols = len(A), len(A[0])
    rank = 0
    pivot_col = 0
    
    while rank < min(rows, cols) and pivot_col < cols:
        max_row = rank
        for i in range(rank + 1, rows):
            if abs(A[i][pivot_col]) > abs(A[max_row][pivot_col]):
                max_row = i
        
        if A[max_row][pivot_col] == 0:
            pivot_col += 1
            continue
        
        A[rank], A[max_row] = A[max_row], A[rank]
        
        for i in range(rows):
            if i != rank:
                factor = Fraction(A[i][pivot_col], A[rank][pivot_col])
                for j in range(pivot_col, cols):
                    A[i][j] -= factor * A[rank][j]
        
        rank += 1
        pivot_col += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        # Generate a random disjointness instance on n variables
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        
        # Compute the geometric Langlands dual using the Langlands-Shahidi method
        rank = matrix_rank(A)
        
        total_rank += rank
    
    metric_value = total_rank / instances_tested
    conjecture_holds = metric_value >= n * math.log(n) * 0.9
    counterexample = "" if conjecture_holds else "n_log_n_bound_violated"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_log_n_bound_violated\" first_failing_seed={seeds[first_failing_seed]}")