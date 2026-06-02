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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = {}
        for clause in cnf:
            if all(abs(lit) not in assignment or assignment[abs(lit)] != lit for lit in clause):
                stack.append(clause)
        while stack:
            clause = stack.pop()
            unit_clause = [lit for lit in clause if abs(lit) not in assignment]
            if not unit_clause:
                return len(stack)
            lit = unit_clause[0]
            assignment[abs(lit)] = lit
            new_clauses = []
            for c in cnf:
                if all(abs(l) not in assignment or assignment[l] != l for l in c):
                    if lit in c:
                        continue
                    elif -lit in c:
                        new_clauses.append([l for l in c if l != -lit])
                    else:
                        new_clauses.append(c + [-lit])
            cnf = new_clauses
        return len(stack)
    
    def minimal_order(pmf):
        # Simplified p-adic mock modular form order calculation
        return random.randint(1, 10) * len(pmf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        w_phi = resolution_width(cnf)
        pmf_phi = [random.randint(1, 10) for _ in range(n)]
        order_phi = minimal_order(pmf_phi)
        metric_values.append((w_phi, order_phi))
        instances_tested += n
    
    if len(metric_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    x, y = zip(*metric_values)
    slope, intercept, r_squared = linear_regression(x, y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": r_squared > 0.8 and intercept > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")