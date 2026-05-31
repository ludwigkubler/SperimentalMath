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
    for i in range(rows):
        # Find pivot
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    gaussian_elimination(matrix)
    rank = 0
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(cols)):
            rank += 1
    return rank

def generate_communication_problem(n):
    # Generate a random linear system Ax = b
    A = [[random.randint(-1, 1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-1, 1) for _ in range(n)]
    return A, b

def aff_roots(A, b):
    # Find the minimal number of affine roots
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    rank_A = rank(augmented_matrix)
    return n - rank_A

def communication_complexity(n):
    # Simplified measure of communication complexity (number of variables)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    aff_roots_sum = 0
    comm_complexity_sum = 0
    aff_roots_squared_sum = 0
    comm_complexity_squared_sum = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            A, b = generate_communication_problem(n)
            aff_roots_val = aff_roots(A, b)
            comm_complexity_val = communication_complexity(n)
            
            instances_tested += 1
            aff_roots_sum += aff_roots_val
            comm_complexity_sum += comm_complexity_val
            aff_roots_squared_sum += aff_roots_val ** 2
            comm_complexity_squared_sum += comm_complexity_val ** 2
    
    if instances_tested == 0:
        return {
            "metric_name": "aff_roots vs comm_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    aff_roots_mean = Fraction(aff_roots_sum, instances_tested)
    comm_complexity_mean = Fraction(comm_complexity_sum, instances_tested)
    aff_roots_variance = (aff_roots_squared_sum - instances_tested * aff_roots_mean ** 2) / instances_tested
    comm_complexity_variance = (comm_complexity_squared_sum - instances_tested * comm_complexity_mean ** 2) / instances_tested
    
    if aff_roots_variance == 0 or comm_complexity_variance == 0:
        return {
            "metric_name": "aff_roots vs comm_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = (instances_tested * aff_roots_sum * comm_complexity_sum - aff_roots_sum * aff_roots_sum * comm_complexity_sum) / (
        math.sqrt(aff_roots_variance * comm_complexity_variance)
    )
    
    return {
        "metric_name": "aff_roots vs comm_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] <= 0.3 for r in results):
        print("RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")