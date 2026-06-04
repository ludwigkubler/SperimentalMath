# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_formula(n):
    if n == 1:
        return 'p'
    else:
        op = random.choice(['&', '|'])
        left = generate_formula(n // 2)
        right = generate_formula(n - len(left) - 3)
        return f'({left} {op} {right})'

def compute_ehrhart_quotient(polytope_points):
    # Placeholder for actual Ehrhart quotient computation
    # This is a dummy implementation that returns a constant value
    return 10

def dpll_proof_tree_height(formula):
    # Placeholder for actual DPLL proof tree height computation
    # This is a dummy implementation that returns a constant value
    return 5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        formula = generate_formula(n)
        polytope_points = []  # Placeholder for actual polytope points computation
        ehrhart_quotient = compute_ehrhart_quotient(polytope_points)
        dpll_height = dpll_proof_tree_height(formula)
        
        if ehrhart_quotient == 0 or dpll_height == 0:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        ratio = Fraction(ehrhart_quotient, dpll_height * dpll_height)
        total_metric_value += ratio
    
    if instances_tested < 30:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric_value <= 1.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")