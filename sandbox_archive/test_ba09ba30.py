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

def generate_tseitin_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for lit in literals:
        clauses.append([lit])
    for i in range(1, n):
        clauses.append([f'~{literals[i-1]}', f'{literals[i]}'])
    clauses.append(['~' + literals[-2], literals[-1]])
    formula = [clauses]
    return formula

def evaluate_polynomial(poly, x_values):
    result = 0
    for term in poly:
        coeff = term[0]
        vars = term[1:]
        value = 1
        for var in vars:
            if var.startswith('~'):
                value *= (1 - x_values[int(var[1:]) - 1])
            else:
                value *= x_values[int(var) - 1]
        result += coeff * value
    return result

def sum_of_abs_roots(poly):
    n = len(poly)
    a = poly[n-1][0]
    b = sum(coeff for i, (coeff, vars) in enumerate(poly) if i < n-1 and 'x' in vars[0])
    c = sum(coeff * x**i for i, (coeff, vars) in enumerate(poly) if i < n-2 and 'x' in vars[0])
    
    if a == 0:
        return float('inf')  # Indeterminate form
    
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return 0  # No real roots
    
    sqrt_discriminant = math.sqrt(discriminant)
    root1 = (-b + sqrt_discriminant) / (2 * a)
    root2 = (-b - sqrt_discriminant) / (2 * a)
    
    return abs(root1) + abs(root2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    sum_abs_root_sum = 0
    sum_proof_length = 0
    
    for n in n_values:
        instances_tested = min(30, n)
        for _ in range(instances_tested):
            formula = generate_tseitin_formula(n)
            poly = [(-1, literals) for literals in formula]
            abs_root_sum = sum_of_abs_roots(poly)
            
            if abs_root_sum == float('inf'):
                continue
            
            proof_length = len(formula)  # Simplified Frege proof length
            total_instances += 1
            sum_abs_root_sum += abs_root_sum
            sum_proof_length += proof_length
    
    if total_instances < 30:
        return {
            "metric_name": "sum_of_abs_roots",
            "metric_value": None,
            "instances_tested": total_instances,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_abs_root_sum = sum_abs_root_sum / total_instances
    mean_proof_length = sum_proof_length / total_instances
    
    correlation_coefficient = (total_instances * sum_abs_root_sum * mean_proof_length -
                               sum_abs_root_sum * sum_proof_length) / (
                                   math.sqrt(total_instances * sum(abs(x**2 for x in abs_root_sum)) - sum_abs_root_sum**2) *
                                   math.sqrt(total_instances * sum(proof_length**2 for proof_length in proof_length) - sum_proof_length**2))
    
    p_value = 1 - math.erf(correlation_coefficient / math.sqrt(2 * (total_instances - 2)))
    
    return {
        "metric_name": "sum_of_abs_roots",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_instances = sum(result["instances_tested"] for result in results)
    mean_abs_root_sum = sum(result["metric_value"] * result["instances_tested"] for result in results) / total_instances
    std_abs_root_sum = math.sqrt(sum((result["metric_value"] - mean_abs_root_sum)**2 * result["instances_tested"] for result in results) / total_instances)
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_abs_root_sum} std={std_abs_root_sum} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_abs_root_sum} std={std_abs_root_sum} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")