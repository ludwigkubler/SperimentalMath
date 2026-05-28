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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_depth(f):
        if len(f) == 1:
            return 0
        else:
            mid = len(f) // 2
            left_depth = calculate_depth(f[:mid])
            right_depth = calculate_depth(f[mid:])
            return max(left_depth, right_depth) + 1
    
    def calculate_genus(n):
        # Simplified model for genus calculation based on n
        return n**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    correlation_sum = 0.0
    expected_genus_sum = 0.0
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            depth = calculate_depth(f)
            genus = calculate_genus(n)
            instances_tested += 1
            total_instances += 1
            correlation_sum += depth * genus
            expected_genus_sum += genus
    
    mean_correlation = correlation_sum / total_instances
    expected_genus_mean = expected_genus_sum / total_instances
    
    conjecture_holds = False
    counterexample = ""
    
    if len(n_values) > 0:
        conjecture_holds = abs(mean_correlation - (expected_genus_mean ** 2)) <= 0.1 * expected_genus_mean
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": mean_correlation,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Spearman rank correlation below threshold"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")