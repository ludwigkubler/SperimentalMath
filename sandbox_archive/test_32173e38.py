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
            return random.choice(['x', '¬x'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['∧', '∨'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def dpll_width(phi):
        if phi == 'x':
            return 1
        elif phi == '¬x':
            return 1
        else:
            subformulas = phi.split()[2:-1]
            return max(dpll_width(sub) for sub in subformulas)
    
    def minimal_group_order(phi):
        n = len(phi)
        if n == 1:
            return 2
        else:
            subformulas = phi.split()[2:-1]
            orders = [minimal_group_order(sub) for sub in subformulas]
            return max(orders) * (len(orders) + 1)
    
    def evaluate_formula(phi):
        if phi == 'x':
            return random.choice([True, False])
        elif phi == '¬x':
            return not evaluate_formula('x')
        else:
            op = phi.split()[1]
            subformulas = phi.split()[2:-1]
            left = evaluate_formula(subformulas[0])
            right = evaluate_formula(subformulas[1])
            if op == '∧':
                return left and right
            elif op == '∨':
                return left or right
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_boolean_formula(n)
        width = dpll_width(phi)
        order = minimal_group_order(phi)
        if evaluate_formula(phi):
            results.append((width, order))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    widths, orders = zip(*results)
    mean_width = sum(widths) / len(widths)
    mean_order = sum(orders) / len(orders)
    correlation = (sum((w - mean_width) * (o - mean_order) for w, o in results) /
                   math.sqrt(sum((w - mean_width)**2 for w in widths) *
                             sum((o - mean_order)**2 for o in orders)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(corr >= 0.5 for corr in [correlation]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        max_correlation = max(result["metric_value"] for result in results if result["conjecture_holds"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")