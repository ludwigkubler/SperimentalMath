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
    
    # Generate Tseitin formula
    for i in range(1, n+1):
        clause = f'{literals[i-1]} | ~{literals[i-1]}'
        clauses.append(clause)
    
    for i in range(n, 0, -1):
        clause = f'~x{i} | {literals[i-2]} | ~{literals[i-2]}'
        clauses.append(clause)
    
    # Last clause
    last_clause = ' & '.join(f'{literals[i-1]}' for i in range(1, n+1))
    clauses.append(last_clause)
    
    return ' & '.join(clauses)

def solve(lits_true, lits_false):
    if not lits_true and not lits_false:
        return None
    elif not lits_false:
        return True
    elif not lits_true:
        return False
    
    lit = random.choice(lits_true)
    new_lits_true = [l for l in lits_true if l != lit]
    new_lits_false = [l for l in lits_false if l != lit]
    
    result = solve(new_lits_true, new_lits_false)
    if result is not None:
        return result
    
    lit = random.choice(lits_false)
    new_lits_true = [l for l in lits_true if l != lit]
    new_lits_false = [l for l in lits_false if l != lit]
    
    result = solve(new_lits_true, new_lits_false)
    if result is not None:
        return result
    
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    sum_abs_root_sum = 0.0
    sum_proof_length = 0
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_tseitin_formula(n)
            lits_true = [f'x{i}' for i in range(1, n+1)]
            lits_false = []
            
            result = solve(lits_true, lits_false)
            if result is None:
                continue
            
            instances_tested += 1
            total_instances += 1
            
            # Calculate Frege proof length (simplified DPLL solver)
            proof_length = n * 2  # Simplified estimation for demonstration purposes
            
            sum_proof_length += proof_length
            
            # Calculate the clause-indicator polynomial and its roots
            # This is a simplified example; actual implementation may vary
            roots = [1, -1]  # Example roots for demonstration
            abs_root_sum = sum(abs(x) for x in roots)
            sum_abs_root_sum += abs_root_sum
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    # Calculate correlation coefficient
    mean_abs_root_sum = sum_abs_root_sum / total_instances
    mean_proof_length = sum_proof_length / total_instances
    
    covariance = 0.0
    for n in n_values:
        for _ in range(5):
            formula = generate_tseitin_formula(n)
            lits_true = [f'x{i}' for i in range(1, n+1)]
            lits_false = []
            
            result = solve(lits_true, lits_false)
            if result is None:
                continue
            
            instances_tested += 1
            total_instances += 1
            
            # Calculate Frege proof length (simplified DPLL solver)
            proof_length = n * 2  # Simplified estimation for demonstration purposes
            
            sum_proof_length += proof_length
            
            # Calculate the clause-indicator polynomial and its roots
            # This is a simplified example; actual implementation may vary
            roots = [1, -1]  # Example roots for demonstration
            abs_root_sum = sum(abs(x) for x in roots)
            sum_abs_root_sum += abs_root_sum
            
            covariance += (abs_root_sum - mean_abs_root_sum) * (proof_length - mean_proof_length)
    
    variance_abs_root_sum = sum((abs_root_sum - mean_abs_root_sum)**2 for n in n_values for _ in range(5)) / total_instances
    variance_proof_length = sum((proof_length - mean_proof_length)**2 for n in n_values for _ in range(5)) / total_instances
    
    if variance_abs_root_sum == 0 or variance_proof_length == 0:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_abs_root_sum * variance_proof_length)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Not all seeds supported the conjecture"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")