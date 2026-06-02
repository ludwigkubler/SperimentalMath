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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def geometric_entropy(f):
    n = len(f)
    p = sum(f) / n
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def circuit_monotone_width(f):
    n = len(f)
    f = [f[i] for i in range(n)]
    
    def is_monotone(g):
        for i in range(len(g)):
            if g[i] == 0:
                continue
            for j in range(i + 1, len(g)):
                if g[j] != g[i]:
                    return False
        return True
    
    max_width = 0
    for k in range(1, n):
        for subset in itertools.combinations(range(n), k):
            g = [f[i] if i in subset else 0 for i in range(n)]
            if is_monotone(g):
                max_width = max(max_width, len(subset))
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_boolean_function(n)
        gamma_f = geometric_entropy(f)
        w_mon_f = circuit_monotone_width(f)
        results.append((gamma_f, w_mon_f))
    
    correlation_coefficient = calculate_correlation(results)
    conjecture_holds = correlation_coefficient >= 0.8
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def calculate_correlation(data):
    n = len(data)
    if n < 2:
        return None
    
    x_sum = sum(x for x, _ in data)
    y_sum = sum(y for _, y in data)
    xy_sum = sum(x * y for x, y in data)
    x_squared_sum = sum(x**2 for x, _ in data)
    y_squared_sum = sum(y**2 for _, y in data)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x_squared_sum - x_sum**2) * (n * y_squared_sum - y_sum**2))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")