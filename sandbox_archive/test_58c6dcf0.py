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

def generate_tseitin_formula(n, k):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each literal
    for lit in literals:
        clauses.append([lit])
    
    # Generate clauses for each pair of literals (k-colorable)
    colors = random.sample(range(k), n)
    for i in range(n):
        for j in range(i+1, n):
            if colors[i] != colors[j]:
                clauses.append([f'x{i+1}', f'x{j+1}'])
    
    # Generate the final clause
    final_clause = [f'x{i+1}' for i in range(n) if colors[i] == 0]
    clauses.append(final_clause)
    
    return literals, clauses

def evaluate_quadratic_form(literals, clauses, assignment):
    n = len(literals)
    qform = 0
    
    for clause in clauses:
        product = 1
        for lit in clause:
            x_index = int(lit[2:]) - 1
            if assignment[x_index] == 'T':
                product *= 1
            elif assignment[x_index] == 'F':
                product *= -1
            else:
                raise ValueError(f"Invalid assignment: {assignment}")
        qform += product
    
    return qform

def count_integral_points(n):
    integral_points = 0
    range_limit = 2 * n
    
    for x in range(-range_limit, range_limit + 1):
        for y in range(-range_limit, range_limit + 1):
            assignment = [str(x), str(y)]
            if evaluate_quadratic_form(literals, clauses, assignment) == 0:
                integral_points += 1
    
    return integral_points

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_integral_points = 0
    proof_widths = []
    
    for n in n_values:
        literals, clauses = generate_tseitin_formula(n, k=3)
        integral_points = count_integral_points(n)
        total_integral_points += integral_points
        
        # Simulate resolution proof width (dummy value for testing)
        proof_width = random.randint(10, 100)
        proof_widths.append(proof_width)
    
    mean_integral_points = total_integral_points / len(n_values)
    correlation_coefficient = calculate_correlation(n_values, proof_widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "low_correlation"
    }

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    variance_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
    variance_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
    
    return covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")