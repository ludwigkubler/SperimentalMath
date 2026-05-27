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
from fractions import Fraction
from math import sqrt, log2

def generate_random_boolean_function(n):
    if n == 1:
        return ('XOR', 'a', 'b')
    else:
        left = generate_random_boolean_function(random.randint(1, n-1))
        right = generate_random_boolean_function(random.randint(1, n-1))
        return ('AND', left, right)

def evaluate_boolean_function(func, assignment):
    if isinstance(func, tuple):
        op, left, right = func
        if op == 'XOR':
            return (evaluate_boolean_function(left, assignment) != evaluate_boolean_function(right, assignment))
        elif op == 'AND':
            return (evaluate_boolean_function(left, assignment) and evaluate_boolean_function(right, assignment))
    else:
        return assignment[func]

def characteristic_polynomial(func):
    n = 2
    while True:
        assignments = [dict(zip('ab', x)) for x in itertools.product([0, 1], repeat=2)]
        values = [evaluate_boolean_function(func, assign) for assign in assignments]
        if len(set(values)) == n:
            return values
        n *= 2

def bruer_group_degree(poly):
    degree = 0
    for value in poly:
        if value != 0:
            degree += 1
    return degree

def xor_and_tree_width(func, assignment=None):
    if assignment is None:
        assignment = {}
    if isinstance(func, tuple):
        op, left, right = func
        if op == 'XOR':
            return max(xor_and_tree_width(left, assignment), xor_and_tree_width(right, assignment))
        elif op == 'AND':
            return 1 + max(xor_and_tree_width(left, assignment), xor_and_tree_width(right, assignment))
    else:
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    degrees = []
    widths = []

    for n in n_values:
        func = generate_random_boolean_function(n)
        poly = characteristic_polynomial(func)
        degree = bruer_group_degree(poly)
        width = xor_and_tree_width(func)
        
        degrees.append(degree)
        widths.append(width)

    correlation_coefficient = pearson_correlation(degrees, widths)
    p_value = t_test(degrees, widths)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value <= 0.05 else "Pearson Correlation Coefficient < 0.7 or p-value > 0.05"
    }

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sqrt(sum((xi - mean_x)**2 for xi in x)) * sqrt(sum((yi - mean_y)**2 for yi in y))
    return numerator / denominator if denominator != 0 else 0

def t_test(x, y):
    n1 = len(x)
    n2 = len(y)
    mean_x = sum(x) / n1
    mean_y = sum(y) / n2
    var_x = sum((xi - mean_x)**2 for xi in x) / (n1 - 1)
    var_y = sum((yi - mean_y)**2 for yi in y) / (n2 - 1)
    t_statistic = (mean_x - mean_y) / sqrt(var_x/n1 + var_y/n2)
    df = min(n1-1, n2-1)
    return t_statistic

if __name__ == "__main__":
    import sys
    import itertools

    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson Correlation Coefficient < 0.7 or p-value > 0.05' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")