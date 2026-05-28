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
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = -A[i][i] / A[i][i]
        for j in range(i+1, n):
            A[j][i] = 0
            for k in range(i+1, n):
                A[j][k] += factor * A[i][k]

    # Back-substitute to find the rank
    rank = n
    for i in range(n-1, -1, -1):
        if all(A[i][j] == 0 for j in range(i+1, n)):
            rank -= 1
        else:
            break
    return rank

def rank(matrix):
    A = [row[:] for row in matrix]
    return gaussian_elimination(A)

def generate_xor_3cnf(n, m):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + ['~' + v for v in variables], 3)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters
    n_values = [5, 10, 15, 20, 30, 40]
    gamma = Fraction(1, 2)  # Example constant for demonstration
    
    results = []
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            clauses = generate_xor_3cnf(n, int(1.5 * n))
            matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            
            minimal_rank = rank(matrix)
            instances_tested += 1
            
            if minimal_rank > gamma * math.log2(n):
                # Construct XOR circuit
                depth = int(1 / gamma) + 1
                conjecture_holds = False
                counterexample = f"n={n}, min_rank={minimal_rank}, depth={depth}"
                break
        
        results.append({
            "metric_name": "min_rank",
            "metric_value": minimal_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric = sum(result["mean_metric"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["mean_metric"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")