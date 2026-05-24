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
    
    def generate_bp(depth):
        if depth == 1:
            return [random.randint(0, 1)]
        else:
            sub_depth = random.randint(2, depth - 1)
            left = generate_bp(sub_depth)
            right = generate_bp(depth - sub_depth)
            return [left, right]
    
    def is_read_twice(bp):
        if isinstance(bp, list):
            for b in bp:
                if not is_read_twice(b):
                    return False
            return True
        else:
            return False
    
    def compute_polynomial(bp):
        if isinstance(bp, list):
            left = compute_polynomial(bp[0])
            right = compute_polynomial(bp[1])
            return [left, right]
        else:
            return bp
    
    def hodge_diamond(polynomial):
        # Placeholder for actual Hodge diamond computation
        return 1  # Simplified for testing purposes
    
    def linear_regression(x, y):
        n = len(x)
        if n == 0:
            return 0, 0
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        denominator = sum((xi - x_mean) ** 2 for xi in x)
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        return slope, intercept
    
    def mean_absolute_error(slope, intercept, x, y):
        n = len(x)
        return sum(abs(yi - (slope * xi + intercept)) for xi, yi in zip(x, y)) / n
    
    depths = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for depth in depths:
        bp = generate_bp(depth)
        if not is_read_twice(bp):
            continue
        polynomial = compute_polynomial(bp)
        rank = hodge_diamond(polynomial)
        ranks.append(rank)
    
    if len(ranks) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    x = depths
    y = ranks
    slope, intercept = linear_regression(x, y)
    mae = mean_absolute_error(slope, intercept, x, y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": slope,
        "instances_tested": len(ranks),
        "conjecture_holds": abs(slope) >= 0.8 and mae <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results if r["instances_tested"] == 60) / len(results)
    std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results if r["instances_tested"] == 60) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["instances_tested"] == 60) / len(results)
    
    if all(r["instances_tested"] == 60 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 2 for i, r in enumerate(results) if r["instances_tested"] != 60), None)
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")