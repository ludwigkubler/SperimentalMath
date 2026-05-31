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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input length must be a power of 2")
    
    def binary_search(left, right):
        if left == right:
            return 1
        mid = (left + right) // 2
        f_left = [f[i] for i in range(2**(mid+1)) if i < 2**mid]
        f_right = [f[i] for i in range(2**(mid+1), 2**(mid+2))]
        return binary_search(left, mid) + binary_search(mid+1, right)
    
    return binary_search(0, n)

def minimal_tropical_motivic_rank(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input length must be a power of 2")
    
    def count_ones(x):
        return bin(x).count('1')
    
    max_ones = 0
    for i in range(2**n):
        max_ones = max(max_ones, count_ones(i))
    
    return max_ones

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        mtr_f = minimal_tropical_motivic_rank(f)
        
        if c_f == 0 or mtr_f == 0:
            continue
        
        results.append((c_f, mtr_f))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    C = [c for c, _ in results]
    R = [r for _, r in results]
    
    mean_C = sum(C) / len(C)
    mean_R = sum(R) / len(R)
    
    covariance = sum((c - mean_C) * (r - mean_R) for c, r in results) / len(results)
    variance_C = sum((c - mean_C)**2 for c in C) / len(C)
    variance_R = sum((r - mean_R)**2 for r in R) / len(R)
    
    correlation_coefficient = covariance / math.sqrt(variance_C * variance_R)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in result and not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")