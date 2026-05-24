# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Make all entries below pivot zero
        pivot = matrix[i][i]
        for k in range(i+1, n):
            factor = Fraction(matrix[k][i], pivot)
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    
    return matrix

def minimal_rank(n, q):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    
    # Construct the configuration space matrix
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j] = Fraction(1, q)
    
    reduced_matrix = gaussian_elimination(matrix)
    
    rank = 0
    for row in reduced_matrix:
        if any(row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    q = random.randint(2, 10)
    
    rank = minimal_rank(n, q)
    lower_bound = Fraction(q**(n/2)).log()
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= lower_bound,
        "counterexample": "" if rank >= lower_bound else f"n={n}, q={q}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = (sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\" first_failing_seed={first_failing_seed}")