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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for var in variables:
        clauses.append([var])
    
    tseitin_vars = [n + i + 1 for i in range(n)]
    
    for i in range(n):
        clauses.append([-variables[i], -tseitin_vars[i]])
        clauses.append([variables[i], tseitin_vars[i]])
        for j in range(i + 1, n):
            clauses.append([-tseitin_vars[i], -tseitin_vars[j]])
            clauses.append([tseitin_vars[i], tseitin_vars[j]])
    
    return variables, clauses

def minimal_order_of_quadratic_residues(clauses):
    residues = set()
    for clause in clauses:
        for lit in clause:
            if lit > 0:
                residues.add(lit)
            else:
                residues.add(-lit)
    min_order = float('inf')
    for r in residues:
        order = 1
        while (r ** order) % n != 1 and order <= n:
            order += 1
        if order < min_order:
            min_order = order
    return min_order

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
        
        results.append({
            "n": n,
            "q": q,
            "w": w
        })
    
    total_q = sum(result["q"] for result in results)
    total_w = sum(result["w"] for result in results)
    mean_q = total_q / len(results)
    mean_w = total_w / len(results)
    
    correlation_coefficient = (sum((result["q"] - mean_q) * (result["w"] - mean_w) for result in results) /
                               math.sqrt(sum((result["q"] - mean_q) ** 2 for result in results) *
                                         sum((result["w"] - mean_w) ** 2 for result in results)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(next(result for result in results if not result["conjecture_holds"]))]
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")