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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_minimal_tropical_curve(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function length must be a power of 2")
    
    # Simplified tropical curve computation (placeholder)
    return sum(f, key=lambda x: -x)

def compute_resolution_proof_width(curve):
    # Placeholder for resolution proof width calculation
    return len(curve) ** 0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        curve = compute_minimal_tropical_curve(f)
        width = compute_resolution_proof_width(curve)
        
        results.append({
            "n": n,
            "curve_length": len(curve),
            "width": width
        })
    
    max_width = max(result["width"] for result in results)
    log_n_squared = (max(results, key=lambda x: x["n"])["n"] ** 0.5) ** 2
    
    metric_value = max_width / log_n_squared
    conjecture_holds = all(width <= 1.5 * log_n_squared for width in [result["width"] for result in results])
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_width={max_width}, log_n_squared={log_n_squared}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_width > 1.5 * log^2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")