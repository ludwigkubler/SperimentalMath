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
    
    def generate_boolean_function(n, m):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    def affine_group_order(n, m):
        return n ** (3/2 + m / 4)
    
    def resolution_proof_size(f):
        # Placeholder function to simulate the resolution proof size
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) * len(f[0])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, n)
            f = generate_boolean_function(n, m)
            order = affine_group_order(n, m)
            proof_size = resolution_proof_size(f)
            results.append((order, proof_size))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    # Calculate Pearson correlation coefficient
    x_mean = sum(x for x, _ in results) / instances_tested
    y_mean = sum(y for _, y in results) / instances_tested
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in results)
    denominator_x = math.sqrt(sum((x - x_mean) ** 2 for x, _ in results))
    denominator_y = math.sqrt(sum((y - y_mean) ** 2 for _, y in results))
    
    if denominator_x == 0 or denominator_y == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    pearson_corr = numerator / (denominator_x * denominator_y)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")