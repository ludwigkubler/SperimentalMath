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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_width(sat_instance):
        n = int(math.log2(len(sat_instance)))
        clauses = []
        for i in range(n):
            clause = random.sample(range(n), 3)
            clauses.append(clause)
        
        stack = [(clauses, [])]
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                return len(assignment)
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment + [literal]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                stack.append((new_clauses, new_assignment))
                continue
            literal = random.choice(clauses[0])
            new_assignment = assignment + [literal]
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.append((new_clauses, new_assignment))
        return len(assignment)
    
    def automorphic_form_order(sat_instance):
        n = int(math.log2(len(sat_instance)))
        truth_table = {i: sat_instance[i] for i in range(len(sat_instance))}
        
        # Simplified encoding of the truth table into a modular form
        order = 1 + sum(truth_table[i] * (2 ** i) for i in range(n))
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        dpll_width_value = dpll_width(sat_instance)
        automorphic_form_order_value = automorphic_form_order(sat_instance)
        
        if dpll_width_value == 0 or automorphic_form_order_value == 0:
            continue
        
        results.append({
            "n": n,
            "dpll_width": dpll_width_value,
            "automorphic_form_order": automorphic_form_order_value
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    n_values = [r["n"] for r in results]
    dpll_widths = [r["dpll_width"] for r in results]
    automorphic_form_orders = [r["automorphic_form_order"] for r in results]
    
    mean_dpll_width = sum(dpll_widths) / len(dpll_widths)
    mean_automorphic_form_order = sum(automorphic_form_orders) / len(automorphic_form_orders)
    
    covariance = sum((d - mean_dpll_width) * (a - mean_automorphic_form_order) for d, a in zip(dpll_widths, automorphic_form_orders))
    variance_dpll_width = sum((d - mean_dpll_width) ** 2 for d in dpll_widths)
    variance_automorphic_form_order = sum((a - mean_automorphic_form_order) ** 2 for a in automorphic_form_orders)
    
    if variance_dpll_width == 0 or variance_automorphic_form_order == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_correlation = covariance / (math.sqrt(variance_dpll_width) * math.sqrt(variance_automorphic_form_order))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_correlation) > 0.5,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first_failing_seed" if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")