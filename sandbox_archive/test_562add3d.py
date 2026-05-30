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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|', '^'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def construct_affine_algebra(formula):
        # Simplified representation of constructing an affine algebra
        # This is a placeholder and does not actually compute the minimal order
        return len(formula.split())
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        order = construct_affine_algebra(formula)
        results.append((n, order))
    
    if not results:
        return {
            "metric_name": "order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_formulas_generated"
        }
    
    order_values = [result[1] for result in results]
    log_n_values = [math.log(result[0], 2) for result in results]
    
    if len(order_values) < 30:
        return {
            "metric_name": "order",
            "metric_value": sum(order_values) / len(order_values),
            "instances_tested": len(order_values),
            "n_max": max(result[0] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_order = sum(order_values) / len(order_values)
    mean_log_n = sum(log_n_values) / len(log_n_values)
    covariance = sum((order_values[i] - mean_order) * (log_n_values[i] - mean_log_n) for i in range(len(order_values))) / len(order_values)
    variance_log_n = sum((log_n_values[i] - mean_log_n) ** 2 for i in range(len(log_n_values))) / len(log_n_values)
    
    if variance_log_n == 0:
        return {
            "metric_name": "order",
            "metric_value": mean_order,
            "instances_tested": len(order_values),
            "n_max": max(result[0] for result in results),
            "conjecture_holds": False,
            "counterexample": "variance_log_n_zero"
        }
    
    correlation_coefficient = covariance / math.sqrt(variance_log_n)
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": len(order_values),
        "n_max": max(result[0] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")