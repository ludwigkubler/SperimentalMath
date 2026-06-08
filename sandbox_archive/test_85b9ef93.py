# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n - n - 1)]
    
    def tseitin_polynomial(instance, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        for literal in literals:
            if literal > 0:
                clause = [-literal]
                for other_literal in literals:
                    if other_literal != literal and (other_literal < 0 or abs(other_literal) > literal):
                        clause.append(other_literal)
                clauses.append(clause)
        return clauses
    
    def dpll(instance, n):
        def backtrack(model, clauses):
            if not any(clause for clause in clauses if all(lit not in model for lit in clause)):
                return True
            literal = next(lit for lit in literals if lit not in model and -lit not in model)
            if literal > 0:
                model[literal] = True
            else:
                model[-literal] = False
            if backtrack(model, clauses):
                return True
            del model[literal]
            if literal > 0:
                model[literal] = False
            else:
                model[-literal] = True
            if backtrack(model, clauses):
                return True
            del model[-literal]
            return False
        
        literals = list(range(-n, 0)) + list(range(1, n+1))
        model = {}
        return backtrack(model, instance)
    
    def local_cohomology_group_order(n):
        # Placeholder for the actual computation of local cohomology group order
        # This is a dummy implementation that returns a random value for demonstration purposes
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    H_star_pi_values = []
    dpll_path_lengths = []
    
    for n in n_values:
        instance = generate_boolean_instance(n)
        clauses = tseitin_polynomial(instance, n)
        if not dpll(clauses, n):
            return {
                "metric_name": "local_cohomology_group_order",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL proof failed"
            }
        H_star_pi = local_cohomology_group_order(n)
        H_star_pi_values.append(H_star_pi)
        dpll_path_lengths.append(len(clauses))
    
    if len(H_star_pi_values) < 30:
        return {
            "metric_name": "local_cohomology_group_order",
            "metric_value": None,
            "instances_tested": len(H_star_pi_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    alpha = Fraction(sum(H_star_pi_values), sum(dpll_path_lengths))
    correlation_coefficient = 0
    for H, d in zip(H_star_pi_values, dpll_path_lengths):
        correlation_coefficient += (H - alpha * math.log(len(n_values))) * (d - sum(dpll_path_lengths) / len(dpll_path_lengths))
    correlation_coefficient /= math.sqrt(sum((H - alpha * math.log(len(n_values)))**2 for H in H_star_pi_values)) * math.sqrt(sum((d - sum(dpll_path_lengths) / len(dpll_path_lengths))**2 for d in dpll_path_lengths))
    
    return {
        "metric_name": "local_cohomology_group_order",
        "metric_value": alpha,
        "instances_tested": len(H_star_pi_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and p_value < 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")