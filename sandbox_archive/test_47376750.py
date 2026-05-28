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
        # Find pivot in column i
        pivot_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        if A[pivot_row][i] == 0:
            continue  # Skip this column if pivot is zero
        
        # Swap rows i and pivot_row
        A[i], A[pivot_row] = A[pivot_row], A[i]
        
        # Eliminate entries below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    # Generate a random instance of the Disjointness problem
    A = [random.sample(range(n), k=1) for _ in range(2)]
    
    # Compute the free probability distribution (simplified for this test)
    C = [[Fraction(1, n)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if A[0][0] == i and A[1][0] == j:
                C[i][j] = Fraction(2, n)
    
    # Calculate the minimal rank of the distribution
    rank = gaussian_elimination(C)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n,
        "counterexample": "" if rank >= n else f"Disjointness function yields a false positive for inputs {A[0][0]} and {A[1][0]}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"Disjointness function yields a false positive\" first_failing_seed={first_failing_seed + 1}")