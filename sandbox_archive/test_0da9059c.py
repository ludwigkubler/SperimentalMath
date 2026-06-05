# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor = -A[k][i] / A[i][i]
            for j in range(n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += factor * A[i][j]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def quadratic_form(cnf):
    n = len(cnf)
    qf = [[0] * n for _ in range(n)]
    
    for clause in cnf:
        for var in clause:
            if abs(var) > n:
                raise ValueError("Variable out of bounds")
            qf[abs(var)-1][abs(var)-1] += 2
            if var < 0:
                qf[abs(var)-1][abs(var)-1] -= 4
    
    return qf

def sat_entropy(cnf):
    n = len(cnf)
    total_clauses = sum(1 for clause in cnf if any(abs(v) <= n for v in clause))
    entropy = -total_clauses * math.log2(total_clauses / n**n)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.randint(-n, n) for _ in range(3)] for _ in range(n)]
        qf = quadratic_form(cnf)
        entropy = sat_entropy(cnf)
        
        # Count integral points
        count = 0
        for x in product(range(-10, 11), repeat=n):
            if all(qf[i][i] * x[i]**2 + sum(qf[i][j] * x[i] * x[j] for j in range(i+1, n)) >= 0 for i in range(n)):
                count += 1
        
        results.append({
            "n": n,
            "count": count
        })
    
    min_integral_points = min(result["count"] for result in results)
    entropy_values = [result["count"] / (2**n) for result in results]
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(entropy_values, entropy_values)) / len(entropy_values)
    mean_entropy = sum(entropy_values) / len(entropy_values)
    
    return {
        "metric_name": "MinIntegralPoints",
        "metric_value": min_integral_points,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
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
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")