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
    
    def generate_instance(n):
        # Generate a random Boolean satisfiability instance with n variables
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause.append(random.choice([-1, 1]) * (n + 1))
            clauses.append(clause)
        return clauses

    def tseitin_formula(clauses):
        # Convert the instance to Tseitin's formula
        n = len(clauses[0])
        literals = [f'x{i+1}' for i in range(n)]
        new_vars = {}
        count = 1
        tseitin_clauses = []
        
        for clause in clauses:
            new_var = f'y{count}'
            new_vars[new_var] = count
            count += 1
            tseitin_clauses.append([new_var, *clause])
            for i in range(n):
                for j in range(i + 1, n):
                    tseitin_clauses.append([-new_var, -literals[i], literals[j]])
                    tseitin_clauses.append([-new_var, literals[i], -literals[j]])
        
        return tseitin_clauses

    def ideal_from_tseitin(tseitin_clauses):
        # Convert Tseitin's formula to an ideal
        n = len(tseitin_clauses[0]) - 1
        variables = [f'x{i+1}' for i in range(n)]
        new_vars = {}
        count = n + 1
        
        for clause in tseitin_clauses:
            if len(clause) > 2:
                new_var = f'y{count}'
                new_vars[new_var] = count
                count += 1
                tseitin_clauses.append([new_var, *clause])
        
        ideal = []
        for var, _ in new_vars.items():
            ideal.append([int(var[1:])])
        
        return ideal

    def singular_homology_order(ideal):
        # Calculate the minimal local homology group order (simplified)
        n = len(ideal)
        return 2 ** (n - 1)

    def resolution_width(tseitin_clauses):
        # Calculate the resolution proof width (simplified)
        max_width = 0
        for clause in tseitin_clauses:
            if len(clause) > max_width:
                max_width = len(clause)
        return max_width

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_instance(n)
        tseitin_clauses = tseitin_formula(instance)
        ideal = ideal_from_tseitin(tseitin_clauses)
        homology_order = singular_homology_order(ideal)
        width = resolution_width(tseitin_clauses)
        
        results.append({
            "n": n,
            "homology_order": homology_order,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "homology_order_over_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    homology_orders = [r["homology_order"] for r in results]
    widths = [r["width"] for r in results]
    
    mean_homology_order = sum(homology_orders) / len(homology_orders)
    mean_width = sum(widths) / len(widths)
    
    correlation_coefficient = 0.0
    if len(homology_orders) > 1 and len(widths) > 1:
        numerator = sum((h - mean_homology_order) * (w - mean_width) for h, w in zip(homology_orders, widths))
        denominator = math.sqrt(sum((h - mean_homology_order) ** 2 for h in homology_orders)) * math.sqrt(sum((w - mean_width) ** 2 for w in widths))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = all(h <= 1.5 * w for h, w in zip(homology_orders, widths)) and correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "homology_order > 1.5*width"
    
    return {
        "metric_name": "homology_order_over_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")