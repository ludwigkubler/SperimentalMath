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
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n+1):
                    matrix[j][k] -= factor * matrix[i][k]

    # Extract the rank
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def quadratic_form(literals, clauses):
    n = len(literals)
    Q = [[0] * n for _ in range(n)]
    
    for clause in clauses:
        literals_in_clause = [lit[2:] for lit in clause.split() if not lit.startswith('~')]
        i = int(literals_in_clause[0]) - 1
        j = int(literals_in_clause[1]) - 1
        Q[i][j] += 1
        Q[j][i] += 1
    
    return gaussian_elimination(Q)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate random Tseitin formula
        for i in range(n):
            clauses.append(f'~{literals[i]} {random.choice(literals)}')
        
        min_rank = quadratic_form(literals, clauses)
        w_G = len(clauses)  # Simplified resolution proof width
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "w_G": w_G
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate correlation coefficient
    x = [result["min_rank"] for result in results]
    y = [result["w_G"] for result in results]
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)
    var_x = sum((x[i] - mean_x)**2 for i in range(n)) / (n - 1)
    var_y = sum((y[i] - mean_y)**2 for i in range(n)) / (n - 1)
    
    correlation_coefficient = cov_xy / math.sqrt(var_x * var_y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.9 and abs(correlation_coefficient - 1) <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")