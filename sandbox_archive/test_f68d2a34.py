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
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / pivot
            for k in range(cols):
                matrix[j][k] += factor * matrix[i][k]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def generate_random_clause_set(n, num_clauses=10):
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        while len(set(clause)) == 1:
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    return clauses

def resolution_width(clauses):
    # Simplified version of resolution width calculation
    return sum(len(set(abs(lit) for lit in clause)) for clause in clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_random_clause_set(n)
        order_A = rank(phi)
        width_w_phi = resolution_width(phi)
        
        if width_w_phi == 0:
            continue
        
        results.append((order_A, width_w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    order_values = [order for order, _ in results]
    width_values = [width for _, width in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    numerator = sum((order - mean_order) * (width - mean_width) for order, width in results)
    denominator = math.sqrt(sum((order - mean_order) ** 2 for order in order_values)) * math.sqrt(sum((width - mean_width) ** 2 for width in width_values))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient <= 1,
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
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")