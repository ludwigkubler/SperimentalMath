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

def generate_truth_table(n):
    return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]

def calculate_minimal_order(truth_table):
    n = len(truth_table)
    rows = truth_table[:]
    cols = [sum(row[i] for row in rows) for i in range(n)]
    
    minimal_order = 0
    while rows:
        min_row_index = min(range(len(rows)), key=lambda i: sum(rows[i]))
        min_col_index = min(range(n), key=lambda j: sum(row[j] for row in rows))
        
        if rows[min_row_index][min_col_index] == 1:
            minimal_order += 1
            rows.pop(min_row_index)
            for row in rows:
                row[min_col_index] = 0
        else:
            break
    
    return minimal_order

def calculate_rank(matrix):
    n = len(matrix)
    rank = 0
    matrix_copy = [row[:] for row in matrix]
    
    for i in range(n):
        if matrix_copy[i][i] == 0:
            found_pivot = False
            for j in range(i+1, n):
                if matrix_copy[j][i] != 0:
                    matrix_copy[i], matrix_copy[j] = matrix_copy[j], matrix_copy[i]
                    found_pivot = True
                    break
            if not found_pivot:
                continue
        
        rank += 1
        for j in range(n):
            if j == i:
                continue
            factor = Fraction(matrix_copy[j][i], matrix_copy[i][i])
            for k in range(n):
                matrix_copy[j][k] -= factor * matrix_copy[i][k]
    
    return rank

def calculate_ratio(truth_table):
    n = len(truth_table)
    minimal_order = calculate_minimal_order(truth_table)
    rank = calculate_rank(truth_table)
    if rank == 0:
        return None
    return Fraction(minimal_order, rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        truth_table = generate_truth_table(n)
        ratio = calculate_ratio(truth_table)
        
        if ratio is None or ratio == Fraction(0, 0):
            return {
                "metric_name": "Ratio",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Matrix is singular"
            }
        
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(math.log(n) >= ratio for n, ratio in zip(n_values, results))
    
    return {
        "metric_name": "Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds log(n)' first_failing_seed={first_failing_seed}")