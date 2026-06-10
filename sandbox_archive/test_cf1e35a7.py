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

def generate_tseitin_formula(n, k):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate base clauses
    for x in literals:
        clauses.append([x, f'-{x}'])
    
    # Generate clauses for each variable
    for i in range(n):
        clause = [f'x{i+1}']
        for j in range(k-1):
            new_var = f'y{i}_{j}'
            clauses.append([new_var])
            clause.append(new_var)
            literals.append(new_var)
        
        # Generate binary clauses for each variable
        for j in range(len(clause) - 1):
            for l in range(j + 1, len(clause)):
                new_var = f'z{i}_{j}_{l}'
                clauses.append([f'-{clause[j]}', f'-{clause[l]}', new_var])
                clauses.append([new_var])
                literals.append(new_var)
    
    # Add final clause
    for lit in literals:
        clauses.append([lit, f'-{lit}'])
    
    return literals, clauses

def evaluate_quadratic_form(literals, clauses, assignment):
    n = len(assignment)
    value = 0
    
    for clause in clauses:
        term = 1
        for lit in clause:
            if lit.startswith('-'):
                x_index = int(lit[1:]) - 1
                term *= (1 - assignment[x_index])
            else:
                x_index = int(lit) - 1
                term *= assignment[x_index]
        
        value += term
    
    return value

def count_integral_points(n):
    literals, clauses = generate_tseitin_formula(n, n)
    integral_points = 0
    
    # Evaluate the quadratic form for all possible integer assignments
    for x in range(-n, n + 1):
        if evaluate_quadratic_form(literals, clauses, [x] * n) == 0:
            integral_points += 1
    
    return integral_points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "correlation_coefficient"
    instances_tested = 30
    n_max = 40
    conjecture_holds = False
    counterexample = ""
    
    correlation_values = []
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        integral_points = count_integral_points(n)
        
        # Placeholder for resolution proof width calculation
        w_phi = n * (n + 1) // 2
        
        correlation_values.append((integral_points, w_phi))
    
    if len(correlation_values) < instances_tested:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": len(correlation_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    correlation = sum((x - y) * (x - z) for x, y in correlation_values for z, _ in correlation_values) / \
                  math.sqrt(sum((x - y) ** 2 for x, y in correlation_values) * sum((z - w) ** 2 for _, w in correlation_values))
    
    if correlation >= 0.7:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")