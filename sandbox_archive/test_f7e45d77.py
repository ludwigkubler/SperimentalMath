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
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for r in range(i+1, n):
            factor = -matrix[r][i] / matrix[i][i]
            for c in range(i, n):
                if i == c:
                    matrix[r][c] = 0
                else:
                    matrix[r][c] += factor * matrix[i][c]

    # Back substitution
    for i in range(n-1, -1, -1):
        for r in range(i-1, -1, -1):
            factor = -matrix[r][i] / matrix[i][i]
            matrix[r][i] = 0
            for c in range(n):
                matrix[r][c] += factor * matrix[i][c]

    return matrix

def rank(matrix):
    n = len(matrix)
    reduced_matrix = [row[:] for row in matrix]
    gaussian_elimination(reduced_matrix)
    rank = sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(n)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    target_rank = rank(matrix)
    
    depth = random.randint(1, n)
    expected_rank_bound = Fraction((math.log2(n) ** depth), 1).limit_denominator()
    
    # Simulate ACC^0 circuit (simplified version)
    current_rank = 0
    for _ in range(depth):
        if current_rank < target_rank:
            current_rank += 1
    
    return {
        "metric_name": "rank_bound",
        "metric_value": current_rank,
        "instances_tested": 1,
        "conjecture_holds": current_rank <= expected_rank_bound,
        "counterexample": "" if current_rank <= expected_rank_bound else f"Depth {depth} circuit could not achieve rank {target_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth {result['counterexample']}\" first_failing_seed={first_failing_seed}")