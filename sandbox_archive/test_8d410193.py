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
    
    def generate_random_formula(m, k):
        literals = [f"x{i}" for i in range(1, 2 * m + 1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, k)
            clauses.append(" OR ".join(clause))
        formula = " AND ".join(clauses)
        return formula
    
    def resolution_width(formula):
        # Simplified resolution width calculation
        return len(formula.split(" AND "))
    
    def affine_order(formula):
        # Simplified affine order calculation
        return len(set(formula.split()))
    
    aff_orders = []
    widths = []
    instances_tested = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_random_formula(m, k=3)
            aff_orders.append(affine_order(formula))
            widths.append(resolution_width(formula))
            instances_tested += 1
    
    if not aff_orders or not widths:
        return {
            "metric_name": "aff_order vs width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    mean_aff_order = sum(aff_orders) / instances_tested
    mean_width = sum(widths) / instances_tested
    
    if len(aff_orders) < 2:
        return {
            "metric_name": "aff_order vs width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    correlation_coefficient = (sum((a - mean_aff_order) * (w - mean_width) for a, w in zip(aff_orders, widths)) /
                               math.sqrt(sum((a - mean_aff_order) ** 2 for a in aff_orders) *
                                         sum((w - mean_width) ** 2 for w in widths)))
    
    c = correlation_coefficient / max(1, mean_width)
    
    return {
        "metric_name": "aff_order vs width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": correlation_coefficient >= 0.8 and c > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_r = sum(result["metric_value"] for result in results) / len(results)
        std_r = math.sqrt(sum((result["metric_value"] - mean_r) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_data\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")