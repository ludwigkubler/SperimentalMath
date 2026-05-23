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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def p_adic_divergence(f, p):
    n = len(f)
    count = 0
    for i in range(2**n):
        if f[i] == 1:
            count += 1
    return Fraction(count, 2**n).log(p)

def communication_complexity_disjointness(n):
    return n

def pearson_correlation_coefficient(data_x, data_y):
    mean_x = sum(data_x) / len(data_x)
    mean_y = sum(data_y) / len(data_y)
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(data_x, data_y)) / len(data_x)
    std_x = (sum((x - mean_x)**2 for x in data_x) / len(data_x))**0.5
    std_y = (sum((y - mean_y)**2 for y in data_y) / len(data_y))**0.5
    return cov_xy / (std_x * std_y)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    data_d_p = []
    data_c_disj = []

    for n in n_values:
        f = generate_boolean_function(n)
        p_adic_val = p_adic_divergence(f, 2)  # Using base 2 for simplicity
        c_disj_val = communication_complexity_disjointness(n)
        data_d_p.append(p_adic_val)
        data_c_disj.append(c_disj_val)

    correlation_coefficient = pearson_correlation_coefficient(data_d_p, data_c_disj)
    mean_metric_value = sum(data_d_p) / len(data_d_p)
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(val <= 10 for val in data_d_p)
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8 or metric_value>10"

    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(data_d_p),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8 or metric_value>10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support")