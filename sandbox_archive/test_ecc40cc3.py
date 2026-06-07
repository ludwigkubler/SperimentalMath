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
    if n <= 0:
        return []
    
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        clauses.append([var])
        clauses.append([-var])
    
    # Generate clauses for implications
    for i in range(n):
        for j in range(i+1, n):
            clauses.append([f'x{i}', -f'x{j}'])
            clauses.append([f'x{j}', -f'x{i}'])
    
    return clauses

def calculate_resolution_width(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            return False
        
        p, _ = random.choice(unit_clauses)
        assignment[p] = True
        new_clauses = []
        for clause in clauses:
            if p not in clause and -p not in clause:
                new_clauses.append(clause)
            elif -p in clause:
                new_clauses.extend([c for c in clause if c != -p])
        
        return dpll(new_clauses, assignment) or dpll(new_clauses, {**assignment, p: False})
    
    assignment = {}
    return len(dpll(clauses, assignment))

def calculate_mge(n):
    # Placeholder function to simulate MGE calculation
    # This is a dummy implementation and should be replaced with actual geometric flow energy calculation
    return random.random() * n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    w_values = []
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        mge_value = calculate_mge(n)
        w_value = calculate_resolution_width(clauses)
        
        mge_values.append(mge_value)
        w_values.append(w_value)
    
    correlation_coefficient = 0
    if len(mge_values) > 1 and len(w_values) > 1:
        mean_mge = sum(mge_values) / len(mge_values)
        mean_w = sum(w_values) / len(w_values)
        
        numerator = sum((m - mean_mge) * (w - mean_w) for m, w in zip(mge_values, w_values))
        denominator = math.sqrt(sum((m - mean_mge)**2 for m in mge_values)) * math.sqrt(sum((w - mean_w)**2 for w in w_values))
        
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    metric_name = "correlation_coefficient"
    metric_value = correlation_coefficient
    instances_tested = len(n_values)
    n_max = max(n_values)
    conjecture_holds = correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient])
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")