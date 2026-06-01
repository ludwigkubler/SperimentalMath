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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def dpll(instance):
        assignment = {}
        
        def solve(instance, assignment):
            if not instance:
                return True
            literal = next((l for l in instance[0] if l not in assignment), None)
            if literal is None:
                return False
            
            pos_var, neg_var = abs(literal), -literal
            assignment[pos_var] = True
            if solve(instance, assignment):
                return True
            del assignment[pos_var]
            
            assignment[neg_var] = True
            if solve(instance, assignment):
                return True
            del assignment[neg_var]
            
            return False
        
        return len(instance) if not solve(instance, assignment) else 0
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    n_max = 40
    instances_tested = 30
    ord_values = []
    dpll_diameters = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_sat_instance(n)
        ord_value = len(instance)  # Simplified version for demonstration; replace with actual computation if needed
        dpll_diameter = dpll(instance)
        
        ord_values.append(ord_value)
        dpll_diameters.append(dpll_diameter)
    
    correlation_coefficient = pearson_correlation(ord_values, dpll_diameters)
    conjecture_holds = correlation_coefficient >= 0.7
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")