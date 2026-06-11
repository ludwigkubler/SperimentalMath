# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def calculate_padic_valuation_degree(clause, p):
    degrees = [abs(int(literal)) for literal in clause if literal != '1' and literal != '-1']
    return min(degrees) if degrees else float('inf')

def generate_random_cnf(num_clauses, seed):
    random.seed(seed)
    literals = ['1', '-1'] + [str(i) for i in range(2, 10)]
    cnf = []
    for _ in range(num_clauses):
        clause = random.sample(literals, random.randint(2, 5))
        cnf.append(' '.join(clause))
    return cnf

def run_trial(seed: int) -> dict:
    num_clauses = 40
    formula = generate_random_cnf(num_clauses, seed)
    clause_depths = [len(clause.split()) for clause in formula]
    min_valuation_degrees = [calculate_padic_valuation_degree(clause, 2) for clause in formula]
    
    if not clause_depths or not min_valuation_degrees:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "empty_clause"
        }
    
    mean_depth = sum(clause_depths) / len(clause_depths)
    mean_valuation = sum(min_valuation_degrees) / len(min_valuation_degrees)
    
    covariance = sum((d - mean_depth) * (v - mean_valuation) for d, v in zip(clause_depths, min_valuation_degrees)) / num_clauses
    variance_depth = sum((d - mean_depth) ** 2 for d in clause_depths) / num_clauses
    variance_valuation = sum((v - mean_valuation) ** 2 for v in min_valuation_degrees) / num_clauses
    
    if variance_depth == 0 or variance_valuation == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": num_clauses,
            "n_max": num_clauses,
            "conjecture_holds": False,
            "counterexample": "constant_values"
        }
    
    correlation_coefficient = covariance / (variance_depth * variance_valuation) ** 0.5
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": num_clauses,
        "n_max": num_clauses,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")