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
import itertools

# Helper functions for polynomial operations and DPLL search tree construction

def poly_from_satsat(phi):
    n = len(phi)
    x = {i: 1 << i for i in range(n)}
    product = 1
    for clause in phi:
        term = 0
        for var in clause:
            if var < 0:
                term |= x[-var]
            else:
                term |= x[var]
        product *= term
    return product

def dpll_search_tree(phi):
    def solve(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            assignment[var] = True
            new_clauses = [c for c in clauses if var not in c and -var not in c]
            return solve(new_clauses, assignment)
        pure_literal = next((v for v in range(1, len(phi) + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal:
            assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return solve(new_clauses, assignment)
        var = next((v for v in range(1, len(phi) + 1)), None)
        assignment[var] = True
        if solve(clauses, assignment):
            return True
        assignment[var] = False
        assignment[-var] = True
        return solve(clauses, assignment)
    assignment = {}
    return solve(phi, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        p = poly_from_satsat(phi)
        d = dpll_search_tree(phi)
        
        if not (isinstance(p, int) and isinstance(d, int)):
            return {
                "metric_name": "qrs_diameter_correlation",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((p, d))
    
    if len(results) < 30:
        return {
            "metric_name": "qrs_diameter_correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    qrs_values = [p % 2 for p, _ in results]
    diameter_values = [d for _, d in results]
    
    mean_qrs = sum(qrs_values) / len(qrs_values)
    mean_diameter = sum(diameter_values) / len(diameter_values)
    
    correlation_sum = sum((q - mean_qrs) * (d - mean_diameter) for q, d in results)
    variance_qrs = sum((q - mean_qrs) ** 2 for q in qrs_values)
    variance_diameter = sum((d - mean_diameter) ** 2 for d in diameter_values)
    
    correlation_coefficient = correlation_sum / (math.sqrt(variance_qrs * variance_diameter))
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(len(results) - 2) / math.sqrt(2)))
    
    return {
        "metric_name": "qrs_diameter_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first_failing_seed" if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")