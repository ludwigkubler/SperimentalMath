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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_matrix_representation(f, n):
    matrix = []
    for i in range(2**n):
        row = []
        for j in range(2**n):
            if (i & j) == 0:
                row.append(f[i ^ j])
            else:
                row.append(0)
        matrix.append(row)
    return matrix

def gaussian_elimination(matrix, n):
    for i in range(n):
        # Find the pivot
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for r in range(i+1, n):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(i, n):
                matrix[r][c] -= factor * matrix[i][c]

def determinant(matrix, n):
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = Fraction(0)
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += (-1) ** c * matrix[0][c] * determinant(submatrix, n-1)
    return det

def alexander_dirac_invariant(matrix):
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be square")
    
    # Perform Gaussian elimination
    gaussian_elimination(matrix, n)
    
    # Calculate the determinant
    det = determinant(matrix, n)
    
    return abs(det)

def communication_complexity_rank(f, n):
    # Placeholder function; actual implementation depends on the specific problem
    # For simplicity, we assume a constant rank for all instances
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        matrix = compute_matrix_representation(f, n)
        
        try:
            alexander_dirac_inv = alexander_dirac_invariant(matrix)
            comm_rank = communication_complexity_rank(f, n)
            results.append((alexander_dirac_inv, comm_rank))
        except Exception as e:
            return {
                "metric_name": "Alex(f) vs. comm_rank(f)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    if not results:
        return {
            "metric_name": "Alex(f) vs. comm_rank(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    alex_values = [r[0] for r in results]
    comm_values = [r[1] for r in results]
    
    mean_alex = sum(alex_values) / len(alex_values)
    mean_comm = sum(comm_values) / len(comm_values)
    
    correlation_coefficient = sum((a - mean_alex) * (c - mean_comm) for a, c in zip(alex_values, comm_values)) / (len(results) * math.sqrt(sum((a - mean_alex)**2 for a in alex_values)) * math.sqrt(sum((c - mean_comm)**2 for c in comm_values)))
    
    return {
        "metric_name": "Alex(f) vs. comm_rank(f)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_range\" first_failing_seed={first_failing_seed}")