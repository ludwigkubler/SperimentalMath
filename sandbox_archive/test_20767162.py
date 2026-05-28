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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = [row[:] for row in matrix]
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(rref[r][i]) > abs(rref[max_row][i]):
                max_row = r
        
        # Swap rows
        rref[i], rref[max_row] = rref[max_row], rref[i]
        
        # Eliminate below pivot
        for r in range(i+1, rows):
            factor = Fraction(-rref[r][i], rref[i][i])
            for c in range(cols):
                rref[r][c] += factor * rref[i][c]
    
    return rref

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def generate_quadratic_form(n, seed):
    random.seed(seed)
    Q = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    Q = [row[:] for row in Q]  # Ensure Q is copied to avoid modifying the original
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        Q = generate_quadratic_form(n, seed)
        min_rank = rank(Q)
        total_rank += min_rank
        instances_tested += 1
    
    mean_rank = total_rank / len(n_values)
    
    if mean_rank <= 3 * math.log(2):  # Assuming α = 2 for simplicity
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Mean rank exceeds O(log(α))"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=... support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds O(log(α))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")