# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f).bit_length() - 1
        # Simplified model: each bit requires 1 bit of communication
        return n
    
    def noncommutative_fourier_transform(f):
        n = len(f)
        transform = [0] * (n + 1)
        for i in range(n + 1):
            sum_val = 0
            for j in range(2**n):
                term = f[j]
                for k in range(i):
                    term *= (-1) ** (j >> k & 1)
                sum_val += term / (2**i)
            transform[i] = sum_val
        return transform
    
    def lp_norm(transform, p):
        norm = 0
        for val in transform:
            norm += abs(val)**p
        return norm**(1/p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        transform = noncommutative_fourier_transform(f)
        lp_norm_value = lp_norm(transform, p=1)  # Assuming p=1 for simplicity
        
        results.append({
            "n": n,
            "communication_complexity": cc,
            "lp_norm_value": lp_norm_value
        })
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    total_cc = sum(result["communication_complexity"] for result in results)
    mean_cc = Fraction(total_cc, len(results))
    std_dev = 0
    for result in results:
        std_dev += (result["communication_complexity"] - mean_cc)**2
    std_dev /= len(results)
    std_dev = std_dev**Fraction(1, 2)
    
    correlation_coefficient = 0
    numerator = sum((result["communication_complexity"] - mean_cc) * (result["lp_norm_value"] - mean_cc) for result in results)
    denominator = len(results) * std_dev * std_dev
    if denominator != 0:
        correlation_coefficient = Fraction(numerator, denominator)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": float(correlation_coefficient),
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient > Fraction(9, 10) and lp_norm_value >= mean_cc * Fraction(4, 5),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "not_enough_support"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")