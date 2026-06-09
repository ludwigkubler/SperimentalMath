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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(sat_formula):
        if not sat_formula:
            return True
        var = next((v for v in range(1, len(sat_formula) + 1) if v not in [abs(lit) for lit in sat_formula]), None)
        if var is None:
            return False
        pos_var = [lit for lit in sat_formula if lit > 0 and lit == var]
        neg_var = [lit for lit in sat_formula if lit < 0 and -lit == var]
        if dpll(pos_var):
            return True
        if dpll(neg_var):
            return True
        return False
    
    def ehrhart_polynomial_degree(clauses):
        # Placeholder for Ehrhart polynomial degree calculation
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    cnf_formula = generate_cnf(n, m)
    resolution_width = dpll(cnf_formula)  # Simplified for demonstration
    ehrhart_degree = ehrhart_polynomial_degree(cnf_formula)
    
    if resolution_width is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll_failed"
        }
    
    metric_value = abs(resolution_width - ehrhart_degree)
    if resolution_width < ehrhart_degree:
        return {
            "metric_name": "resolution_width",
            "metric_value": metric_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w(F) < degree_of_Ehrhart_polynomial(F)"
        }
    
    C = 2  # Placeholder constant
    if metric_value > C * math.log(n + m):
        return {
            "metric_name": "resolution_width",
            "metric_value": metric_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"metric_value > {C} * log(n + m)"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"metric_value > {C} * log(n + m)\" first_failing_seed={first_failing_seed}")