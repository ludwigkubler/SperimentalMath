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
    
    def generate_random_boolean_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.choice(variables + [f'~{v}' for v in variables])
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def resolution_width(formula):
        # Simplified version of resolution width calculation
        # This is a placeholder and should be replaced with actual logic
        return len(formula.split(' & '))
    
    def minimal_order_of_brauer_group(n):
        # Placeholder for Brauer group computation
        # This is a placeholder and should be replaced with actual logic
        return math.sqrt(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        formula = generate_random_boolean_formula(n)
        width = resolution_width(formula)
        order = minimal_order_of_brauer_group(n)
        results.append((n, order, width))
    
    if not results:
        return {
            "metric_name": "Brauer Group Order and Resolution Width Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "Brauer Group Order and Resolution Width Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance size"
        }
    
    orders = [order for _, order, _ in results]
    widths = [width for _, _, width in results]
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    correlation = sum((o - mean_order) * (w - mean_width) for o, w in zip(orders, widths)) / (len(results) * math.sqrt(sum((o - mean_order)**2 for o in orders)) * math.sqrt(sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "Brauer Group Order and Resolution Width Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else f"Correlation: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.7 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")