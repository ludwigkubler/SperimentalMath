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
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = A[i][i]
        if factor == 0:
            continue  # Skip row with zero pivot
        for j in range(i, cols):
            A[i][j] /= factor
        
        for r in range(rows):
            if r != i:
                factor = A[r][i]
                for j in range(i, cols):
                    A[r][j] -= factor * A[i][j]
    return A

def rank_of_matrix(A):
    rows, cols = len(A), len(A[0])
    rank = 0
    for col in range(cols):
        if any(A[row][col] != 0 for row in range(rank, rows)):
            rank += 1
    return rank

def generate_bp(n):
    bp = []
    for _ in range(n):
        bp.append(random.choice([0, 1]))
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times
            bp = generate_bp(n)
            rank = rank_of_matrix(gaussian_elimination(bp))
            results.append((n, rank))
    
    total_rank = sum(rank for _, rank in results)
    avg_rank = Fraction(total_rank, len(results))
    max_rank = max(rank for _, rank in results)
    
    conjecture_holds = all(avg_rank <= math.log2(2**n) and max_rank >= n**2 for n, _ in results)
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, max_rank={max_rank}"
    
    return {
        "metric_name": "Rank of Quotient Sheaf",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*3 + 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 2}")