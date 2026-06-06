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
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        pivot = matrix[i][i]
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], pivot)
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def variance_ratio(matrix):
    n = len(matrix)
    sum_elements = 0
    sum_squares = 0
    for i in range(n):
        for j in range(i, n):
            sum_elements += matrix[i][j]
            sum_squares += matrix[i][j] ** 2
    
    mean = Fraction(sum_elements, n * (n + 1) // 2)
    variance = Fraction(sum_squares - n * (n + 1) * (2 * n + 1) / 12, n * (n + 1) // 2)
    return float(variance / mean)

def minimal_order(formal_context):
    n = len(formal_context)
    order = 0
    for i in range(n):
        for j in range(i+1, n):
            if formal_context[i][j] == 1:
                order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        matrix = gaussian_elimination(instance)
        variance = variance_ratio(matrix)
        min_order_val = minimal_order(instance)
        
        if variance == 0:
            continue
        
        ratio = Fraction(min_order_val, variance)
        results.append(ratio)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    
    conjecture_holds = all(0.5 <= r <= 2 for r in results)
    counterexample = "" if conjecture_holds else "Ratio out of bounds"
    
    return {
        "metric_name": "Min Order / Variance Ratio",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(5, 10, 15, 20, 30, 40),  # All tested sizes are at least 5
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            print("RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed=", seed)
            sys.exit(0)
    
    mean_value = sum(trial["metric_value"] for trial in results) / len(results)
    std_dev = math.sqrt(sum((trial["metric_value"] - mean_value) ** 2 for trial in results) / len(results))
    support_fraction = sum(trial["conjecture_holds"] for trial in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")