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

def minimal_order_of_quadratic_residues(clauses):
    residues = set()
    for clause in clauses:
        for lit in clause:
            if lit.startswith('x'):
                residues.add(int(lit[1:]))
    return min(residues) if residues else None

def generate_tseitin_formula(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for var in variables:
        clauses.append([var])
        clauses.append([-var])
    
    def tseitin_encode(i, j, k):
        clause = [-i, -j, k]
        clauses.append(clause)
        return k
    
    m = 0
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            k = f"y{m}"
            m += 1
            tseitin_encode(i, j, k)
    
    for i in range(1, n+1):
        k = f"z{i}"
        clauses.append([k] + [f"-x{j}" for j in range(1, n+1) if j != i])
    
    return variables, clauses

def resolution_width(clauses):
    # Simplified version of resolution width calculation
    # This is a placeholder and should be replaced with actual implementation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        q = minimal_order_of_quadratic_residues(clauses)
        w = resolution_width(clauses)
        
        if q is not None and w is not None:
            results.append((q, w))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    q_values = [q for q, _ in results]
    w_values = [w for _, w in results]
    
    mean_q = sum(q_values) / len(q_values)
    std_q = math.sqrt(sum((x - mean_q) ** 2 for x in q_values) / len(q_values))
    mean_w = sum(w_values) / len(w_values)
    std_w = math.sqrt(sum((x - mean_w) ** 2 for x in w_values) / len(w_values))
    
    correlation = sum((q_values[i] - mean_q) * (w_values[i] - mean_w) for i in range(len(q_values))) / (len(q_values) * std_q * std_w)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")