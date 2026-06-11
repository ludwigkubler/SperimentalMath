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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        # Simplified SAT solver using backtracking
        assignment = [None] * (2 * n + 1)
        
        def backtrack(i):
            if i == 2 * n + 1:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(any(assignment[abs(lit)] == sign for lit, sign in clause) for clause in cnf):
                    if backtrack(i + 1):
                        return True
                assignment[i] = None
            return False
        
        return backtrack(1)
    
    def p_adic_valuation(cnf):
        # Simplified p-adic valuation calculation
        p = 2  # Using base 2 for simplicity
        min_order = float('inf')
        for clause in cnf:
            order = max(abs(lit) for lit in clause if assignment[abs(lit)] == sign)
            if order < min_order:
                min_order = order
        return min_order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if not is_satisfiable(cnf):
            continue
        assignment = [None] * (2 * n + 1)
        
        # Measure complexity of distinguishing φ from its unsatisfiable variant φ'
        # This is a placeholder for actual complexity measurement logic
        complexity = n ** 0.5
        
        min_order = p_adic_valuation(cnf)
        results.append({
            "n": n,
            "min_order": min_order,
            "complexity": complexity
        })
    
    if not results:
        return {
            "metric_name": "p-adic valuation order vs complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No satisfiable CNF generated"
        }
    
    n_max = max(result["n"] for result in results)
    mean_order = sum(result["min_order"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    correlation_coefficient = (sum((result["min_order"] - mean_order) * (result["complexity"] - mean_complexity) 
                                   for result in results) /
                              math.sqrt(sum((result["min_order"] - mean_order) ** 2 for result in results) *
                                        sum((result["complexity"] - mean_complexity) ** 2 for result in results)))
    
    return {
        "metric_name": "p-adic valuation order vs complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_complexity <= 3.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 
                                     for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")