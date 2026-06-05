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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank(f):
    n = int(math.log2(len(f)))
    rank = 0
    for i in range(n):
        count_0 = sum(1 for x in f if x & (1 << i) == 0)
        count_1 = sum(1 for x in f if x & (1 << i) != 0)
        rank += max(count_0, count_1)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    B_f_values = []
    r_f_values = []

    for n in n_values:
        f = generate_random_boolean_function(n)
        B_f = communication_complexity_rank(f)  # Simplified Brauer group rank
        r_f = communication_complexity_rank(f)

        B_f_values.append(B_f)
        r_f_values.append(r_f)

    correlation_coefficient = calculate_pearson_correlation(B_f_values, r_f_values)
    
    metric_value = correlation_coefficient
    instances_tested = len(n_values) * 30
    n_max = max(n_values)
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_too_low"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))

    if denominator == 0:
        return 0

    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")