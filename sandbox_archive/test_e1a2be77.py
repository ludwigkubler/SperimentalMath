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
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_random_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            op = random.choice(['&', '|', '^'])
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def construct_affine_algebra(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 1
        elif formula.startswith('(') and formula.endswith(')'):
            left, op, right = formula[1:-1].split()
            if op == '&':
                return max(construct_affine_algebra(left), construct_affine_algebra(right))
            elif op == '|':
                return max(construct_affine_algebra(left), construct_affine_algebra(right))
            elif op == '^':
                return 1 + max(construct_affine_algebra(left), construct_affine_algebra(right))
        else:
            return 2
    
    def log_n(n):
        if n <= 0:
            return 0
        return math.log2(n)
    
    results = []
    for n in range(5, 41):
        formula = generate_random_boolean_formula(n)
        order = construct_affine_algebra(formula)
        results.append((n, order))
    
    if not results:
        return {
            "metric_name": "order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_values = [r[0] for r in results]
    order_values = [r[1] for r in results]
    mean_order = sum(order_values) / len(order_values)
    log_n_values = [log_n(n) for n in n_values]
    
    if not all(log_n_val > 0 for log_n_val in log_n_values):
        return {
            "metric_name": "order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "log_n_zero_or_negative"
        }
    
    correlation = sum((x - mean_order) * (y - mean_log_n) for x, y in zip(order_values, log_n_values)) / len(order_values)
    mean_log_n = sum(log_n_values) / len(log_n_values)
    
    return {
        "metric_name": "order",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")