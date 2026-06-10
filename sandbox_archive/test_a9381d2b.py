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
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left.split()))
            op = random.choice(['&', '|'])
            return f'({left} {op} {right})'

    def dpll_search_tree_depth(formula):
        if formula == 'x':
            return 0
        left, op, right = formula[1:-1].split()
        return max(dpll_search_tree_depth(left), dpll_search_tree_depth(right)) + 1

    def tropical_hodge_index(formula):
        if formula == 'x':
            return 1
        left, op, right = formula[1:-1].split()
        return max(tropical_hodge_index(left), tropical_hodge_index(right))

    n_values = [5, 10, 15, 20, 30, 40]
    thi_values = []
    dpll_depths = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            thi_value = tropical_hodge_index(formula)
            dpll_depth = dpll_search_tree_depth(formula)
            thi_values.append(thi_value)
            dpll_depths.append(dpll_depth)

    n_max = max(n_values)
    instances_tested = len(thi_values)
    correlation_coefficient = calculate_correlation(thi_values, dpll_depths)

    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
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

    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    variance_x = sum((xi - mean_x) ** 2 for xi in x) / n
    variance_y = sum((yi - mean_y) ** 2 for yi in y) / n

    return covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")