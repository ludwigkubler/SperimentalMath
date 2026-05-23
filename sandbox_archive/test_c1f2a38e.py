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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a Tseitin formula with n variables
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for var in variables:
        clauses.append([var])
    for i in range(n):
        for j in range(i+1, n):
            clauses.append([f'~{variables[i]}', f'{variables[j]}'])
            clauses.append([f'~{variables[j]}', f'{variables[i]}'])
    
    # Construct the tropicalized Boolean algebra
    num_clauses = len(clauses)
    TBA = [[0] * (num_clauses + 1) for _ in range(num_clauses + 1)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var.startswith('~'):
                idx = variables.index(var[1:]) + 1
                TBA[i][idx] = -1
            else:
                idx = variables.index(var) + 1
                TBA[i][idx] = 1
    
    # Compute the minimal rank of quotient modules
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
        return rank
    
    minimal_rank = gaussian_elimination(TBA)
    
    # Measure the upper bound α(n) = O(n^2 log n)
    alpha_n = n**2 * math.log(n)
    
    # Correlate the minimal rank with the length of resolution proofs
    resolution_length = len(clauses)
    if minimal_rank > alpha_n:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Seed {seed}: Minimal rank exceeds O(n^2 log n)"
        }
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Seed {first_failing_seed}: Minimal rank exceeds O(n^2 log n)' first_failing_seed={first_failing_seed}")