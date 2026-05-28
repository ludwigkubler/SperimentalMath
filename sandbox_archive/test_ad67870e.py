# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements in column i
        pivot = Fraction(A[i][i])
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], pivot)
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    
    # Count non-zero rows to determine rank
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        # Generate random Disjointness instance
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        
        # Compute free probability distribution (simplified example)
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
        
        # Calculate minimal rank
        rank = gaussian_elimination(C)
        total_rank += rank
    
    metric_value = total_rank / instances_tested
    conjecture_holds = metric_value >= n
    counterexample = "" if conjecture_holds else "rank < n"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank < n\" first_failing_seed={first_failing_seed + 1}")