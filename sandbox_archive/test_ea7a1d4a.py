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
    
    def dpll(sat_formula):
        if not sat_formula:
            return True
        for literal in sat_formula[0]:
            new_formula = [clause for clause in sat_formula[1:] if literal not in clause and -literal not in clause]
            if dpll(new_formula):
                return True
            new_formula = [clause for clause in sat_formula[1:] if -literal not in clause]
            if dpll(new_formula):
                return True
        return False

    def min_order_quadratic_form(n):
        # Placeholder implementation, actual method needed
        return n  # Simplified example
    
    def monotone_width(sat_formula):
        # Placeholder implementation, actual method needed
        return len(sat_formula)  # Simplified example
    
    instances_tested = 0
    total_order = 0
    total_width = 0
    n_max = 5
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        variables = list(range(n))
        clauses = []
        for _ in range(2**n):
            clause = [random.choice(variables) + 1]
            clauses.append(clause)
        
        if dpll(clauses):
            instances_tested += 1
            order = min_order_quadratic_form(n)
            width = monotone_width(clauses)
            total_order += order
            total_width += width
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * mean_order * mean_width - 
                                sum(order * width for order, width in zip([mean_order] * instances_tested, [mean_width] * instances_tested))) / \
                               math.sqrt((instances_tested * mean_order**2 - sum(order**2 for order in [mean_order] * instances_tested)) *
                                         (instances_tested * mean_width**2 - sum(width**2 for width in [mean_width] * instances_tested)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")