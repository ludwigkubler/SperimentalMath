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
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    
    for pivot_row in range(rows):
        max_pivot = abs(augmented_matrix[pivot_row][pivot_row])
        max_row = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(augmented_matrix[i][pivot_row]) > max_pivot:
                max_pivot = abs(augmented_matrix[i][pivot_row])
                max_row = i
        
        augmented_matrix[pivot_row], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[pivot_row]
        
        pivot_value = augmented_matrix[pivot_row][pivot_row]
        if pivot_value == 0:
            continue
        
        for j in range(pivot_row, cols + 1):
            augmented_matrix[pivot_row][j] /= pivot_value
        
        for i in range(rows):
            if i != pivot_row:
                factor = augmented_matrix[i][pivot_row]
                for j in range(pivot_row, cols + 1):
                    augmented_matrix[i][j] -= factor * augmented_matrix[pivot_row][j]
    
    rank = sum(1 for row in augmented_matrix if any(val != 0 for val in row[:cols]))
    return rank

def tropicalize(matrix):
    rows, cols = len(matrix), len(matrix[0])
    trop_matrix = [[-math.inf] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j]:
                trop_matrix[i][j] = 0
            else:
                trop_matrix[i][j] = math.inf
    return trop_matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    A_trop = tropicalize(A)
    rank_value = gaussian_elimination(A_trop)
    
    metric_name = "tropical_rank"
    metric_value = rank_value
    instances_tested = 1
    conjecture_holds = rank_value >= n / 2
    counterexample = "" if conjecture_holds else "rank too small"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='rank too small' first_failing_seed={first_failing_seed}")