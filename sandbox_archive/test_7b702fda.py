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
        factor = Fraction(1, A[i][i])
        for k in range(i+1, n):
            A[k][i] *= factor
        
        # Eliminate above
        for k in range(i):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    
    return sum(abs(A[i][i]) for i in range(n))

def generate_read_once_bp(n):
    bp = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            bp[i][j] = random.choice([0, 1])
            bp[j][i] = bp[i][j]
    return bp

def generate_read_twice_bp(n):
    bp = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            bp[i][j] = random.choice([0, 1])
            bp[j][i] = random.choice([0, 1])
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        read_once_bp = generate_read_once_bp(n)
        read_twice_bp = generate_read_twice_bp(n)
        
        read_once_rank = gaussian_elimination(read_once_bp)
        read_twice_rank = gaussian_elimination(read_twice_bp)
        
        results.append({
            "n": n,
            "read_once_rank": read_once_rank,
            "read_twice_rank": read_twice_rank
        })
    
    mean_read_once_rank = sum(result["read_once_rank"] for result in results) / len(results)
    mean_read_twice_rank = sum(result["read_twice_rank"] for result in results) / len(results)
    
    conjecture_holds = all(mean_read_twice_rank <= 2 * math.log(n) and mean_read_once_rank >= n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Non-Commutative Rank Gap",
        "metric_value": (mean_read_twice_rank, mean_read_once_rank),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_read_twice_rank = sum(res["metric_value"][0] for res in results) / len(results)
    mean_read_once_rank = sum(res["metric_value"][1] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean_read_twice_rank={mean_read_twice_rank} mean_read_once_rank={mean_read_once_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")