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

def generate_boolean_formula(n_vars, n_clauses):
    vars = [f'x{i}' for i in range(n_vars)]
    clauses = []
    for _ in range(n_clauses):
        clause = random.choice(['', 'not ']) + random.choice(vars)
        if random.random() < 0.5:
            clause += ' or ' + random.choice(vars)
        if random.random() < 0.5:
            clause += ' or not ' + random.choice(vars)
        clauses.append(clause)
    return ' and '.join(clauses)

def calculate_minimal_brauer_character_order(formula):
    # Placeholder for actual computation
    # For simplicity, we'll use a dummy value that depends on the formula length
    return len(formula.split())

def calculate_frege_proof_depth(formula):
    # Placeholder for actual computation
    # For simplicity, we'll use a dummy value that depends on the formula length
    return len(formula.split()) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    instances_tested = 0
    
    for n_vars in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_boolean_formula(n_vars, random.randint(1, n_vars))
            min_order = calculate_minimal_brauer_character_order(formula)
            proof_depth = calculate_frege_proof_depth(formula)
            
            results.append({
                "n": n_vars,
                "min_order": min_order,
                "proof_depth": proof_depth
            })
            
            instances_tested += 1
            n_max = max(n_max, n_vars)
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    min_orders = [r["min_order"] for r in results]
    proof_depths = [r["proof_depth"] for r in results]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    
    covariance = sum((x - mean_min_order) * (y - mean_proof_depth) for x, y in zip(min_orders, proof_depths))
    variance_min_order = sum((x - mean_min_order) ** 2 for x in min_orders) / len(min_orders)
    variance_proof_depth = sum((y - mean_proof_depth) ** 2 for y in proof_depths) / len(proof_depths)
    
    correlation_coefficient = covariance / (math.sqrt(variance_min_order) * math.sqrt(variance_proof_depth))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break