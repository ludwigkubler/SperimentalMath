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

def calculate_padic_valuation_degree(clause, p):
    degrees = [abs(int(literal)) for literal in clause.split() if literal != '1' and literal != '-1']
    return min(degrees) if degrees else float('inf')

def generate_random_cnf(num_clauses, seed):
    random.seed(seed)
    literals = ['x' + str(i) for i in range(1, 6)] + ['-x' + str(i) for i in range(1, 6)]
    formula = []
    for _ in range(num_clauses):
        clause = random.sample(literals, 3)
        formula.append(' '.join(clause))
    return formula

def run_trial(seed: int) -> dict:
    num_clauses = 40
    formula = generate_random_cnf(num_clauses, seed)
    clause_depths = [len(clause.split()) for clause in formula]
    min_valuation_degrees = [calculate_padic_valuation_degree(clause, 2) for clause in formula]
    
    if not min_valuation_degrees or not clause_depths:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    mean_valuation = sum(min_valuation_degrees) / len(min_valuation_degrees)
    mean_depth = sum(clause_depths) / len(clause_depths)
    
    covariance = sum((min_valuation_degrees[i] - mean_valuation) * (clause_depths[i] - mean_depth) for i in range(num_clauses)) / num_clauses
    variance_valuation = sum((min_valuation_degrees[i] - mean_valuation) ** 2 for i in range(num_clauses)) / num_clauses
    variance_depth = sum((clause_depths[i] - mean_depth) ** 2 for i in range(num_clauses)) / num_clauses
    
    if variance_valuation == 0 or variance_depth == 0:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "constant_values"
        }
    
    correlation = covariance / (math.sqrt(variance_valuation) * math.sqrt(variance_depth))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": num_clauses,
        "n_max": num_clauses,
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")