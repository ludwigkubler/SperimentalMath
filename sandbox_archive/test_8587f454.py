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
    n = 40
    p = 0.5
    
    # Generate Erdős–Rényi graph
    adjacency_matrix = [[random.random() < p for _ in range(n)] for _ in range(n)]
    for i in range(n):
        adjacency_matrix[i][i] = 0
    
    # Compute Laplacian matrix
    laplacian = [[sum(1 - adjacency_matrix[i][j] for j in range(n) if i != j) if i == j else -adjacency_matrix[i][j] for j in range(n)] for i in range(n)]
    
    # Compute second-largest eigenvalue of the Laplacian matrix
    lambda_2 = second_largest_eigenvalue(laplacian)
    if lambda_2 is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Construct Tseitin formula and run DPLL-based SAT solver
    resolution_length = run_dpll_solver(laplacian)
    if resolution_length is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "solver_failed"
        }
    
    # Verify the conjecture
    c = Fraction(1, 2)  # Example constant, adjust as needed
    if math.log2(resolution_length) >= c * lambda_2 * n:
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: lambda_2={lambda_2}, n={n}, resolution_length={resolution_length}"
        }

def second_largest_eigenvalue(matrix):
    def power_iteration(matrix, v, max_iter=1000):
        for _ in range(max_iter):
            v = [sum(matrix[i][j] * v[j] for j in range(len(v))) for i in range(len(v))]
            norm = math.sqrt(sum(x**2 for x in v))
            if norm == 0:
                return None
            v = [x / norm for x in v]
        return v
    
    def rayleigh_quotient(matrix, v):
        numerator = sum(matrix[i][j] * v[i] * v[j] for i in range(len(v)) for j in range(len(v)))
        denominator = sum(v[i]**2 for i in range(len(v)))
        if denominator == 0:
            return None
        return numerator / denominator
    
    def find_second_largest_eigenvalue(matrix, max_iter=1000):
        v = [random.random() for _ in range(len(matrix))]
        lambda_1 = None
        lambda_2 = None
        
        for _ in range(max_iter):
            v = power_iteration(matrix, v)
            if lambda_1 is None:
                lambda_1 = rayleigh_quotient(matrix, v)
            else:
                lambda_2 = rayleigh_quotient(matrix, v)
                if lambda_2 is not None and (lambda_2 > lambda_1 or (lambda_2 == lambda_1 and lambda_2 != 0)):
                    lambda_1, lambda_2 = lambda_2, lambda_1
        
        return lambda_2
    
    return find_second_largest_eigenvalue(matrix)

def run_dpll_solver(laplacian):
    # Placeholder for DPLL solver implementation
    # This is a dummy function and should be replaced with actual DPLL code
    return None

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")