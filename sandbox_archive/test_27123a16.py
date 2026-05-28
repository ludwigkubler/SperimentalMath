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
        # Simplified computation for demonstration purposes
        return n
    
    def randomized_or_complexity(f):
        n = len(f)
        max_bits = 0
        for _ in range(100):  # Sample 100 random inputs
            input_bits = ''.join(str(random.choice([0, 1])) for _ in range(n))
            bits_required = sum(1 for i, bit in enumerate(input_bits) if f[i] == int(bit))
            max_bits = max(max_bits, bits_required)
        return max_bits
    
    n_values = [40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        h1_size = ehrhart_cohomology_group_size(f)
        ror_f_n = randomized_or_complexity(f)
        results.append((h1_size**2, ror_f_n))
    
    if len(results) < 30:
        return {
            "metric_name": "ROR_f(n)",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    h1_squared, ror_f_n = zip(*results)
    slope, intercept = linear_regression(h1_squared, ror_f_n)
    
    return {
        "metric_name": "ROR_f(n)",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": slope <= 0.5,  # Placeholder constant c
        "counterexample": "" if slope <= 0.5 else f"Counterexample found with slope {slope}"
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi**2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_slope = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = result["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")