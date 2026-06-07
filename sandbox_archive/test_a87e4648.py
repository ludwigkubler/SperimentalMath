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
    if n <= 1:
        return []
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate binary clauses for each variable
    for i in range(1, n + 1):
        clauses.append((i,))
        clauses.append((-i,))
    
    # Generate clauses for implications
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append((i, -j))
            clauses.append((-i, j))
    
    return variables, clauses

def dpll_solver(clauses, assignment):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = literal > 0
        return dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    
    literal, _ = random.choice(clauses)
    new_assignment1 = assignment.copy()
    new_assignment1[abs(literal)] = literal > 0
    if dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment1):
        return True
    
    new_assignment2 = assignment.copy()
    new_assignment2[abs(literal)] = literal < 0
    if dpll_solver([c for c in clauses if literal not in c and -literal not in c], new_assignment2):
        return True
    
    return False

def calculate_resolution_width(clauses):
    assignment = {}
    return len(dpll_solver(clauses, assignment))

def geometric_flow_energy(n):
    # Placeholder function to simulate MGE calculation
    return random.uniform(0.5 * n, 1.5 * n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = generate_tseitin_formula(n)
        mge = geometric_flow_energy(n)
        w = calculate_resolution_width(clauses)
        
        if mge is None or w is None:
            return {
                "metric_name": "MGE vs Resolution Width",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((mge, w))
    
    if not results:
        return {
            "metric_name": "MGE vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 1,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    mge_values, w_values = zip(*results)
    correlation_coefficient = sum((m - mean_mge) * (w - mean_w) for m, w in zip(mge_values, w_values)) / (len(results) * math.sqrt(sum((m - mean_mge) ** 2 for m in mge_values) * sum((w - mean_w) ** 2 for w in w_values)))
    mean_mge = sum(mge_values) / len(mge_values)
    mean_w = sum(w_values) / len(w_values)
    
    return {
        "metric_name": "MGE vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")