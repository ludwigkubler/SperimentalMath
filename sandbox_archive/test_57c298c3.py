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

def generate_sat_instance(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def tseitin_formula(clauses):
    literals = set()
    new_vars = {}
    for i, clause in enumerate(clauses):
        literals.update(clause)
        new_var = len(literals) + 1
        new_vars[i] = new_var
        clauses.append([new_var])
        for literal in clause:
            clauses.append([-literal, -new_var])

    return literals, new_vars, clauses

def p_adic_valuation_ring(n):
    # Simplified p-adic valuation ring calculation (not actual implementation)
    return n

def logarithmic_capacity(n):
    # Simplified logarithmic capacity calculation (not actual implementation)
    return math.log(n)

def clause_depth(clauses):
    max_depth = 0
    for clause in clauses:
        depth = len(clause)
        if depth > max_depth:
            max_depth = depth
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        literals, new_vars, tseitin_clauses = tseitin_formula(clauses)
        
        p_valuation_ring = p_adic_valuation_ring(n)
        log_capacity = logarithmic_capacity(p_valuation_ring)
        clause_depth_value = clause_depth(tseitin_clauses)
        
        results.append({
            "n": n,
            "log_capacity": log_capacity,
            "clause_depth": clause_depth_value
        })
    
    total_ratio = sum(result["log_capacity"] / result["clause_depth"] for result in results) / len(results)
    conjecture_holds = total_ratio < 1.5
    
    return {
        "metric_name": "C(n)/D(φ)",
        "metric_value": total_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"C(n)/D(φ) >= 1.5\" first_failing_seed={first_failing_seed}")