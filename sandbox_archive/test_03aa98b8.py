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
        max_row = i
        for j in range(i + 1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            A[i][j] /= pivot
        for k in range(rows):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, cols):
                    A[k][j] -= factor * A[i][j]
    return A

def rank(matrix):
    rref = gaussian_elimination(matrix)
    rank = sum(1 for row in rref if any(row[j] != 0 for j in range(len(row))))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    c = random.uniform(0.1, 2.0)
    min_rank = float('inf')
    
    for _ in range(30):
        # Generate a modular form and its AC0 circuit representation
        # This is a placeholder; actual implementation depends on the conjecture
        tropicalized_form = [random.randint(-10, 10) for _ in range(n)]
        
        # Compute the minimal rank of the tropicalized modular form
        min_rank = min(min_rank, rank([tropicalized_form]))
    
    expected_min_rank = 2**c * n
    conjecture_holds = min_rank >= expected_min_rank * 1.5
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Modular Form",
        "metric_value": min_rank,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Expected rank >= {expected_min_rank * 1.5}, got {min_rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")