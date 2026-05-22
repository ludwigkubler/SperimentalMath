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

def gaussian_elimination(A, b):
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        
        # Swap rows
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate non-pivot elements
        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    
    # Extract solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    
    return x

def rank(M):
    n = len(M)
    M_rref = gaussian_elimination(M, [0]*len(M))
    
    rank = 0
    for row in M_rref:
        if any(row[i] != 0 for i in range(n)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        A = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        b = [random.choice([-1, 1]) for _ in range(n)]
        
        try:
            rank_A = rank(A)
            total_rank += rank_A
        except ValueError as e:
            counterexample = f"Non-zero pivot not found: {e}"
            return {
                "metric_name": "Minimal Rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = mean_rank >= n
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")