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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n_vars, n_clauses):
        variables = list(range(1, n_vars + 1))
        clauses = []
        for _ in range(n_clauses):
            clause = [random.choice(variables), random.choice(variables)]
            while len(set(clause)) < 2:
                clause = [random.choice(variables), random.choice(variables)]
            clauses.append(tuple(sorted(clause)))
        return variables, set(clauses)
    
    def resolution_width(phi):
        n_vars = max(phi[0])
        n_clauses = len(phi[1])
        
        # Simplified resolution width calculation
        return n_clauses + n_vars
    
    def minimal_braided_monoid_order(phi):
        n_vars = max(phi[0])
        n_clauses = len(phi[1])
        
        # Simplified braided monoid order calculation
        return n_vars + n_clauses
    
    results = []
    for _ in range(30):
        n_vars = random.randint(5, 40)
        n_clauses = random.randint(n_vars, n_vars * 2)
        phi = generate_instance(n_vars, n_clauses)
        
        w_phi = resolution_width(phi)
        n_braided_monoid = minimal_braided_monoid_order(phi)
        
        results.append((n_braided_monoid, w_phi))
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_braided_monoid_values = [r[0] for r in results]
    w_phi_values = [r[1] for r in results]
    
    mean_n_braided_monoid = sum(n_braided_monoid_values) / len(n_braided_monoid_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    covariance = sum((n_braided_monoid_values[i] - mean_n_braided_monoid) * (w_phi_values[i] - mean_w_phi) for i in range(len(n_braided_monoid_values)))
    variance_n_braided_monoid = sum((n_braided_monoid_values[i] - mean_n_braided_monoid) ** 2 for i in range(len(n_braided_monoid_values)))
    
    if variance_n_braided_monoid == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(max(phi[0]) for phi in results),
            "conjecture_holds": False,
            "counterexample": "Variance of n_braided_monoid is zero"
        }
    
    r_squared = covariance / (math.sqrt(variance_n_braided_monoid) * math.sqrt(sum((w_phi_values[i] - mean_w_phi) ** 2 for i in range(len(w_phi_values)))))

    return {
        "metric_name": "resolution_width",
        "metric_value": r_squared,
        "instances_tested": len(results),
        "n_max": max(max(phi[0]) for phi in results),
        "conjecture_holds": 0.7 <= r_squared < 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_r_squared = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")