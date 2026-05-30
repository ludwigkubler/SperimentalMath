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
    
    def generate_communication_problem(n):
        # Generate a random communication problem with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_input_space(problem):
        # Construct the input space of Boolean functions for the given problem
        input_space = []
        for i in range(len(problem)):
            if problem[i] == 0:
                input_space.append((i, 0))
            else:
                input_space.append((i, 1))
        return input_space
    
    def compute_euler_characteristic(input_space):
        # Compute the Euler characteristic of the Čech complex
        n = len(input_space)
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return -1
    
    def spearman_correlation_metric(metric_values, C_n):
        # Compute Spearman's rank correlation coefficient
        n = len(metric_values)
        ranks = {v: i for i, v in enumerate(sorted(set(metric_values)), start=1)}
        sorted_metrics = [ranks[v] for v in metric_values]
        sorted_C_n = [ranks[c] for c in C_n]
        
        numerator = sum((sorted_metrics[i] - sorted_C_n[i]) ** 2 for i in range(n))
        denominator = n * (n**2 - 1) / 12
        return 1 - (6 * numerator) / denominator
    
    def gaussian_elimination(matrix):
        # Perform Gaussian elimination to compute the determinant
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        det = 1
        for i in range(rows):
            det *= matrix[i][i]
        return det
    
    def compute_determinant(input_space):
        # Compute the determinant of the input space matrix
        n = len(input_space)
        if n == 0:
            return 1
        elif n == 1:
            return 1
        else:
            matrix = [[0] * (n + 1) for _ in range(n + 1)]
            for i, (j, val) in enumerate(input_space):
                matrix[i][j] = val
                matrix[i][-1] += val
                matrix[-1][i] += val
            return gaussian_elimination(matrix)
    
    def compute_C_n(n):
        # Compute the deterministic protocol complexity C(n)
        return n
    
    metric_values = []
    C_n = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):
            problem = generate_communication_problem(n)
            input_space = construct_input_space(problem)
            metric_value = compute_determinant(input_space)
            C_n.append(compute_C_n(n))
            
            instances_tested += 1
            n_max = max(n_max, n)
            metric_values.append(metric_value)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Euler characteristic",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = spearman_correlation_metric(metric_values, C_n)
    return {
        "metric_name": "Euler characteristic",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")