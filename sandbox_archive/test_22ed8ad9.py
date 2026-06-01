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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(boolean_function):
        n = len(boolean_function)
        tropical_matrix = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if boolean_function[i] == 1 and boolean_function[j] == 1:
                    tropical_matrix[i][j] = max(i, j)
        return tropical_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for r in range(i+1, n):
                if matrix[r][i] > matrix[max_row][i]:
                    max_row = r
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate below pivot
            for r in range(i+1, n):
                factor = Fraction(matrix[r][i], matrix[i][i])
                for c in range(i, n):
                    matrix[r][c] -= factor * matrix[i][c]
        
        # Back-substitute to find solution
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = Fraction(matrix[i][-1], matrix[i][i])
            for j in range(i+1, n):
                solution[i] -= solution[j] * matrix[i][j]
        return solution
    
    def minimal_local_ring_unit_group_size(tropical_matrix):
        n = len(tropical_matrix)
        identity = [[0 if i == j else -math.inf for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [-1] for row in tropical_matrix] + identity
        solution = gaussian_elimination(augmented_matrix)
        return max(solution) + 1
    
    def communication_complexity_rank(boolean_function):
        n = len(boolean_function)
        # Placeholder for actual computation; currently just returns a dummy value
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            boolean_function = generate_boolean_function(n)
            tropical_matrix = tropicalize(boolean_function)
            unit_group_size = minimal_local_ring_unit_group_size(tropical_matrix)
            rank = communication_complexity_rank(boolean_function)
            
            total_metric_value += unit_group_size * rank
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_metric = total_metric_value / instances_tested
    return {
        "metric_name": "Correlation",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,  # Placeholder; actual correlation check not implemented
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")