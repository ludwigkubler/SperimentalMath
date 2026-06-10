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
    
    def polynomial_from_boolean_function(f):
        n = len(next(iter(f.keys())))
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        for x, y in f.items():
            poly[x][y] = 1
        return poly
    
    def minimal_tropical_derivative(poly):
        n = len(poly)
        mt = [0] * n
        for i in range(n):
            for j in range(n):
                if poly[i][j] == 1:
                    mt[i] = max(mt[i], j)
        return mt
    
    def communication_complexity_rank_variance(f):
        n = len(next(iter(f.keys())))
        ranks = [len([x for x, y in f.items() if x == i]) for i in range(n)]
        mean_rank = sum(ranks) / n
        variance = sum((r - mean_rank) ** 2 for r in ranks) / n
        return variance
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def generate_boolean_function(n):
        f = {}
        for x in range(1 << n):
            y = random.randint(0, 1)
            f[x] = y
        return f
    
    metric_name = "correlation_coefficient"
    instances_tested = 30
    n_max = 40
    mt_values = []
    rc_values = []
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        poly = polynomial_from_boolean_function(f)
        mt = minimal_tropical_derivative(poly)
        rc = communication_complexity_rank_variance(f)
        mt_values.append(sum(mt) / n)
        rc_values.append(rc)
    
    if len(mt_values) == 0 or len(rc_values) == 0:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric"
        }
    
    correlation_coefficient = correlation(mt_values, rc_values)
    conjecture_holds = 0.7 <= correlation_coefficient <= 0.9
    counterexample = "" if conjecture_holds else f"correlation={correlation_coefficient}"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(0.7 <= r["metric_value"] < 0.9 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")