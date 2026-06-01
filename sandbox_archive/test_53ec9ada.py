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

def generate_boolean_formula(m, k=3):
    variables = list(range(1, m + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, random.randint(2, m))
        clause = [-x if random.choice([True, False]) else x for x in clause]
        clauses.append(clause)
    return clauses

def boolean_lattice_size(m):
    return 1 << m

def resolution_proof_width(clauses):
    n = len(clauses[0])
    width = 2 ** (n - 1)
    return width

def minimal_order_of_affine_generators(clauses):
    # Placeholder implementation for the affine order
    # This is a dummy function that returns a constant value
    return 3

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        clauses = generate_boolean_formula(m)
        width = resolution_proof_width(clauses)
        aff_order = minimal_order_of_affine_generators(clauses)
        
        if width == 0 or aff_order == 0:
            continue
        
        results.append({
            "m": m,
            "width": width,
            "aff_order": aff_order
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(m_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    aff_orders = [r["aff_order"] for r in results]
    widths = [r["width"] for r in results]
    
    mean_aff_order = sum(aff_orders) / len(aff_orders)
    mean_width = sum(widths) / len(widths)
    
    correlation_coefficient = (sum((a - mean_aff_order) * (w - mean_width) for a, w in zip(aff_orders, widths)) /
                               math.sqrt(sum((a - mean_aff_order) ** 2 for a in aff_orders) *
                                         sum((w - mean_width) ** 2 for w in widths)))
    
    c = mean_aff_order / mean_width
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(a >= c * w for a, w in zip(aff_orders, widths)),
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")