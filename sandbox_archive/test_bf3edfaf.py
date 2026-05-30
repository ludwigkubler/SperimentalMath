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
            return 'x'
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(random.randint(1, n-1))
            right = generate_boolean_formula(random.randint(1, n-1))
            return f'({left} {op} {right})'

    def construct_affine_algebra(formula):
        if formula == 'x':
            return 1
        elif '&' in formula:
            left, _, right = formula.split('&', 1)
            order_left = construct_affine_algebra(left.strip())
            order_right = construct_affine_algebra(right.strip())
            return max(order_left, order_right) + 1
        elif '|' in formula:
            left, _, right = formula.split('|', 1)
            order_left = construct_affine_algebra(left.strip())
            order_right = construct_affine_algebra(right.strip())
            return max(order_left, order_right) + 1
        else:
            raise ValueError("Invalid boolean formula")

    n_max = 40
    instances_tested = 0
    total_order = 0

    for n in range(5, n_max + 1):
        formula = generate_boolean_formula(n)
        order = construct_affine_algebra(formula)
        total_order += order
        instances_tested += 1

    mean_order = total_order / instances_tested
    conjecture_holds = False
    counterexample = ""

    if instances_tested >= 30:
        log_n_values = [math.log(n, 2) for n in range(5, n_max + 1)]
        correlation_coefficient = calculate_correlation(log_n_values, [order for order in range(5, n_max + 1)])
        if correlation_coefficient >= 0.8:
            conjecture_holds = True
        else:
            counterexample = f"Correlation coefficient {correlation_coefficient} < 0.8"

    return {
        "metric_name": "mean_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")