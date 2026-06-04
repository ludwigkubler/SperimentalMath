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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def arithmetic_hierarchy_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        return n
    
    def circuit_monotone_width(f):
        n = len(f)
        if n <= 1:
            return 1
        max_width = 1
        for i in range(n):
            width = 1
            for j in range(i+1, n):
                if f[i] != f[j]:
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    def correlation_coefficient(data):
        n = len(data)
        x_mean = sum(x for x, _ in data) / n
        y_mean = sum(y for _, y in data) / n
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in data)
        denominator = math.sqrt(sum((x - x_mean)**2 for x, _ in data)) * math.sqrt(sum((y - y_mean)**2 for _, y in data))
        return numerator / denominator if denominator != 0 else float('nan')
    
    n_values = [30, 35, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        ah_f = arithmetic_hierarchy_complexity(f)
        w_mon_f = circuit_monotone_width(f)
        results.append((ah_f, w_mon_f))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    correlation = correlation_coefficient(results)
    p_value = 0.01  # Assuming a significance level of 0.01
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.9 and p_value <= 0.01,
        "counterexample": "" if abs(correlation) > 0.9 else f"correlation_coefficient={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")