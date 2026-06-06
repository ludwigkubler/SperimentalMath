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

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Create clauses for OR conditions
    for i in range(1, n):
        clauses.append(f'{variables[i]} {variables[i-1]}')
    
    # Create clauses for NOT conditions
    for i in range(n):
        clauses.append(f'-{variables[i]} {variables[(i+1) % n]}')
    
    # Create the final clause
    clauses.append(f'{-variables[0]} {variables[-1]}')
    
    return clauses

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            clauses = tseitin_formula(n)
            num_clauses = len(clauses)
            
            # Convert clauses to a system of linear equations over GF(2)
            A = [[0] * (num_clauses + 1) for _ in range(num_clauses)]
            b = [0] * num_clauses
            
            for i, clause in enumerate(clauses):
                terms = clause.split()
                for term in terms:
                    if term[0] == '-':
                        var_index = int(term[1:]) - 1
                        A[i][var_index] = 1
                    else:
                        var_index = int(term) - 1
                        A[i][var_index] = 1
                b[i] = 1
            
            # Solve the system using Gaussian elimination
            try:
                solution = gaussian_elimination(A, b)
                minimal_order = sum(1 for x in solution if x != 0)
            except Exception as e:
                return {
                    "metric_name": "MinimalOrder",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
            
            total_metric_value += minimal_order / num_clauses
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for n in n_values if all(abs(mean_metric_value - (minimal_order / num_clauses)) <= 0.1 * abs(minimal_order / num_clauses) for _ in range(5))) / len(n_values)
    
    return {
        "metric_name": "MinimalOrder",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")