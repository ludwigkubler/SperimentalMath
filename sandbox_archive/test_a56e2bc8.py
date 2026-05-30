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
    
    def evaluate_boolean_function(f, x):
        result = f[0]
        for i in range(1, len(f)):
            if x & (1 << (len(f) - i - 1)):
                result = f[i] ^ result
        return result
    
    def compute_invariant_generators(n):
        # Placeholder function to simulate invariant generator computation
        # This is a dummy implementation and should be replaced with actual logic
        return [i for i in range(2**n) if evaluate_boolean_function(generate_boolean_function(n), i) == 0]
    
    n_values = [5, 10, 15, 20, 30, 40]
    invariant_counts = []
    n_max = 0
    
    for n in n_values:
        n_max = max(n_max, n)
        f = generate_boolean_function(n)
        I_f = compute_invariant_generators(n)
        invariant_counts.append(len(I_f))
    
    if not invariant_counts:
        return {
            "metric_name": "invariant_count",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(invariant_counts) / len(invariant_counts)
    std_dev = (sum((x - mean)**2 for x in invariant_counts) / len(invariant_counts))**0.5
    
    correlation_coefficient = 0
    n_sqrt_log_n = [n**0.5 * math.log(n) for n in n_values]
    
    if len(n_sqrt_log_n) > 1 and std_dev > 0:
        numerator = sum((invariant_counts[i] - mean) * (n_sqrt_log_n[i] - sum(n_sqrt_log_n) / len(n_sqrt_log_n)) for i in range(len(invariant_counts)))
        denominator = len(invariant_counts) * std_dev * math.sqrt(sum((x - sum(n_sqrt_log_n) / len(n_sqrt_log_n))**2 for x in n_sqrt_log_n))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = 0.8 <= correlation_coefficient >= 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient_out_of_range"
    
    return {
        "metric_name": "invariant_count",
        "metric_value": mean,
        "instances_tested": len(invariant_counts),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")