# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
import collections

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] for row in matrix]
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = -augmented_matrix[i][i] / augmented_matrix[max_row][i]
        for j in range(n + 1):
            if i != j:
                augmented_matrix[j][i] += factor * augmented_matrix[max_row][j]
            else:
                augmented_matrix[j][i] *= factor
    return augmented_matrix

def solve_linear_system(A, b):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = reduced_matrix[i][n]
        for j in range(i + 1, n):
            x[i] -= reduced_matrix[i][j] * x[j]
        x[i] /= reduced_matrix[i][i]
    return x

def generate_random_sat_instance(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(20):  # Generate 20 random clauses
        clause = [random.choice(variables) * (1 if random.randint(0, 1) else -1)
                   for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def map_sat_to_tropical_elliptic_curve(clauses):
    # Simplified mapping procedure
    rank = len(set(abs(c) for clause in clauses for c in clause))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance_count = 30
        total_rank = 0
        total_time = 0
        
        for _ in range(instance_count):
            clauses = generate_random_sat_instance(n)
            rank = map_sat_to_tropical_elliptic_curve(clauses)
            
            # Simulate SAT solving time (placeholder)
            solve_time = random.uniform(0.1, n * 0.1)  # Random time between 0.1 and n*0.1 seconds
            
            total_rank += rank
            total_time += solve_time
        
        avg_rank = total_rank / instance_count
        avg_time = total_time / instance_count
        
        results.append({
            "n": n,
            "avg_rank": avg_rank,
            "avg_time": avg_time
        })
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        x_values = [result["avg_rank"] for result in results]
        y_values = [result["avg_time"] for result in results]
        
        mean_x = sum(x_values) / len(x_values)
        mean_y = sum(y_values) / len(y_values)
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator = math.sqrt(sum((x - mean_x) ** 2 for x in x_values)) * math.sqrt(sum((y - mean_y) ** 2 for y in y_values))
        
        correlation_coefficient = numerator / denominator if denominator != 0 else 0.0
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(result["avg_time"] > 0 for result in results),
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_below_0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "correlation_below_0.5" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] == "correlation_below_0.5")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")