# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_polynomial(n, d):
    coeffs = [random.randint(1, 10) for _ in range(d + 1)]
    x = 'x'
    return sum(c * x**i for i, c in enumerate(coeffs))

def evaluate_polynomial(p, n):
    x_values = [2**i for i in range(n)]
    results = []
    for x_val in x_values:
        result = 0
        term = 1
        for coeff in p.split('x'):
            if 'x' in coeff:
                power = int(coeff[coeff.index('x') + 1:])
                result += int(coeff[:coeff.index('x')]) * (x_val ** power)
            else:
                result += int(coeff)
        results.append(result)
    return results

def schur_weyl_rank(p):
    # Placeholder for actual Schur-Weyl rank calculation
    # This is a dummy implementation and should be replaced with the actual logic
    return len(p.split('x'))  # Simplified for demonstration purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(1, n // 2)
    
    p = generate_polynomial(n, d)
    results = evaluate_polynomial(p, n)
    rank = schur_weyl_rank(p)
    
    if rank == 0:
        return {
            "metric_name": "circuit_depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    depth = sum(results) / len(results)
    metric_value = rank ** 2
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": abs(depth - metric_value) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_depth = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_depth)**2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")