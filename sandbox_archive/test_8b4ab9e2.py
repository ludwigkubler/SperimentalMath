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
    
    def generate_instance(n):
        return [random.randint(1, n) for _ in range(n)]
    
    def compute_local_ring_norm(instance):
        norm = 0
        for x in instance:
            norm += x ** 2
        return math.sqrt(norm)
    
    def compute_growth_rate(instance):
        growth_rate = 0
        for i in range(1, len(instance)):
            growth_rate += abs(instance[i] - instance[i-1])
        return growth_rate
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_instance(n)
        norm = compute_local_ring_norm(instance)
        growth_rate = compute_growth_rate(instance)
        metric_values.append((norm, growth_rate))
    
    if len(metric_values) < 2:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def pearson_correlation(values):
        x_mean = sum(x for x, _ in values) / len(values)
        y_mean = sum(y for _, y in values) / len(values)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in values)
        denominator = math.sqrt(sum((x - x_mean) ** 2 for x, _ in values)) * math.sqrt(sum((y - y_mean) ** 2 for _, y in values))
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation(metric_values)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient <= n_max ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")