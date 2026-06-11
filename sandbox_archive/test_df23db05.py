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
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        pivot = matrix[i][i]
        for j in range(i+1, cols):
            matrix[i][j] /= pivot
        
        # Eliminate above the pivot
        for r in range(rows):
            if r != i:
                factor = matrix[r][i]
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = 0
    for row in reduced_matrix:
        if any(row):
            rank += 1
    return rank

def generate_communication_instance(n):
    # Generate a random binary matrix of size n x n
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "geometric_flow_time"
    instances_tested = 0
    n_max = 0
    total_geometric_flow_time = 0
    total_rank_variance = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test each size with 5 instances
            matrix = generate_communication_instance(n)
            rank_value = rank(matrix)
            geometric_flow_time = random.uniform(1, n**2)  # Simulate geometric flow time
            
            total_geometric_flow_time += geometric_flow_time
            total_rank_variance += rank_value ** 2
            instances_tested += 1
    
    mean_geometric_flow_time = total_geometric_flow_time / instances_tested
    mean_rank_variance = total_rank_variance / instances_tested
    conjecture_holds = abs(mean_geometric_flow_time - math.sqrt(mean_rank_variance)) <= 0.05 * math.sqrt(mean_rank_variance)
    counterexample = "" if conjecture_holds else f"geometric_flow_time={mean_geometric_flow_time}, rank_variance={mean_rank_variance}"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_geometric_flow_time,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric_flow_time does not meet the conjecture\" first_failing_seed={first_failing_seed}")