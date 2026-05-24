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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_tropical_curve(f):
        n = len(f)
        if n == 1:
            return f[0]
        else:
            mid = n // 2
            left = generate_random_boolean_function(mid)
            right = generate_random_boolean_function(n - mid)
            curve = [max(left[i], right[i]) for i in range(n)]
            return sum(curve, key=lambda x: -x)
    
    def compute_resolution_proof_width(f):
        n = len(f)
        if n == 1:
            return 0
        else:
            mid = n // 2
            left = generate_random_boolean_function(mid)
            right = generate_random_boolean_function(n - mid)
            width_left = compute_resolution_proof_width(left)
            width_right = compute_resolution_proof_width(right)
            return max(width_left, width_right) + 1
    
    def log_squared(n):
        if n <= 0:
            return 0
        return math.log2(n) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        curve = compute_minimal_tropical_curve(f)
        width = compute_resolution_proof_width(f)
        widths.append(width)
    
    mean_width = sum(widths) / len(widths)
    max_width = max(widths)
    log2_n = math.log2(len(widths))
    upper_bound = 1.5 * log2_n ** 2
    
    conjecture_holds = max_width <= upper_bound
    counterexample = "" if conjecture_holds else f"max_width={max_width}, upper_bound={upper_bound}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_width,
        "instances_tested": len(widths),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_width_exceeds_upper_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")