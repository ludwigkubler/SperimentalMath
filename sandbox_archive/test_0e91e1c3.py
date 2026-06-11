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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def twisted_quandle_action(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 2
        else:
            left, op, right = formula[1:-1].split()
            if op == '&':
                return twisted_quandle_action(left) * twisted_quandle_action(right)
            elif op == '|':
                return twisted_quandle_action(left) + twisted_quandle_action(right)
    
    def resolution_proof_width(formula):
        if formula == '0' or formula == '1':
            return 1
        else:
            left, op, right = formula[1:-1].split()
            if op == '&':
                return max(resolution_proof_width(left), resolution_proof_width(right))
            elif op == '|':
                return 1 + max(resolution_proof_width(left), resolution_proof_width(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        order = twisted_quandle_action(formula)
        width = resolution_proof_width(formula)
        results.append((order, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    
    cov = sum((o - mean_order) * (w - mean_width) for o, w in results) / len(results)
    var_order = sum((o - mean_order) ** 2 for o in orders) / len(orders)
    var_width = sum((w - mean_width) ** 2 for w in widths) / len(widths)
    
    correlation_coefficient = cov / math.sqrt(var_order * var_width)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")