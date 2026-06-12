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

def generate_formula(n):
    literals = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals, 2)
        clauses.append(f"({clause[0]} | {clause[1]})")
    return " & ".join(clauses)

def dpll_width(formula):
    if formula == "":
        return 0
    if " | " not in formula:
        return 1
    left, right = formula.split(" | ", 1)
    return max(dpll_width(left), dpll_width(right))

def twisted_hodge_order(n):
    # Placeholder function for the minimal order of a twisted Hodge structure
    # This is a dummy implementation and should be replaced with actual computation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        width = dpll_width(formula)
        order = twisted_hodge_order(n)
        
        if width == 0:
            continue
        
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders, widths = zip(*results)
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((o - mean_order) * (w - mean_width) for o, w in results) /
                   math.sqrt(sum((o - mean_order)**2 for o in orders) *
                             sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    correlations = []
    instances_tested = 0
    n_max = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["metric_value"] is not None:
            correlations.append(trial_result["metric_value"])
            instances_tested += trial_result["instances_tested"]
            n_max = max(n_max, trial_result["n_max"])
    
    mean_correlation = sum(correlations) / len(correlations)
    support_fraction = sum(1 for c in correlations if abs(c) >= 0.8) / len(correlations)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={math.sqrt(sum((c - mean_correlation)**2 for c in correlations) / len(correlations))} support_fraction={support_fraction}")
    elif any(abs(c) < 0.8 for c in correlations):
        first_failing_seed = seeds[correlations.index(next(c for c in correlations if abs(c) < 0.8))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")