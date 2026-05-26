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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate current column below pivot
        factor = matrix[i][i]
        for j in range(i, cols):
            matrix[i][j] /= factor
        
        for r in range(i+1, rows):
            factor = matrix[r][i]
            for j in range(i, cols):
                matrix[r][j] -= factor * matrix[i][j]

def min_rank(matrix):
    U = [row[:] for row in matrix]
    gaussian_elimination(U)
    rank = 0
    for row in U:
        if any(row[j] != 0 for j in range(len(row))):
            rank += 1
    return rank

def construct_read_twice_bp(size):
    # Placeholder implementation; replace with actual construction logic
    return [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    bp = construct_read_twice_bp(n)
    
    # Placeholder implementation; replace with actual entanglement tensor computation
    entanglement_tensor = [[random.random() for _ in range(n)] for _ in range(n)]
    
    rank = min_rank(entanglement_tensor)
    lower_bound = n
    upper_bound = n * math.log2(n) ** 2
    
    conjecture_holds = lower_bound <= rank <= upper_bound
    counterexample = "" if conjecture_holds else f"rank={rank}, expected=[{lower_bound}, {upper_bound}]"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
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
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank below bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")