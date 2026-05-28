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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def ehrhart_cohomology_group_size(f):
        n = int(math.log2(len(f)))
        # Simplified Ehrhart cohomology group size calculation
        return (2**(n-1)) * len(f)
    
    def randomized_or_complexity(f):
        n = int(math.log2(len(f)))
        max_bits = 0
        for _ in range(100):  # Sample 100 random inputs
            input_bits = ''.join(str(bit) for bit in random.sample(range(n), n))
            bits_needed = len(input_bits)
            if bits_needed > max_bits:
                max_bits = bits_needed
        return max_bits
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi**2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def is_valid_instance(f):
        cohomology_size = ehrhart_cohomology_group_size(f)
        or_complexity = randomized_or_complexity(f)
        if cohomology_size == 0:
            return False
        return or_complexity <= 2 * cohomology_size**2
    
    n_values = [40, 41, 42, 43]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        if not is_valid_instance(f):
            return {
                "metric_name": "Randomized OR Complexity",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        cohomology_size = ehrhart_cohomology_group_size(f)
        or_complexity = randomized_or_complexity(f)
        results.append((cohomology_size**2, or_complexity))
    
    if len(results) < 30:
        return {
            "metric_name": "Randomized OR Complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    slope, _ = linear_regression([x for x, y in results], [y for x, y in results])
    return {
        "metric_name": "Randomized OR Complexity",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": slope <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_slope = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")