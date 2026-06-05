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
    
    def generate_instance(n):
        return [random.randint(1, n) for _ in range(n)]
    
    def calculate_minimal_order(instance):
        # Placeholder function to simulate minimal order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(instance))
    
    def calculate_communication_complexity_rank(instance):
        # Placeholder function to simulate communication complexity rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(instance)) ** 2
    
    n_samples = 30
    sum_m = 0
    sum_r = 0
    sum_m2 = 0
    sum_r2 = 0
    
    for _ in range(n_samples):
        instance = generate_instance(random.randint(5, 40))
        m = calculate_minimal_order(instance)
        r = calculate_communication_complexity_rank(instance)
        
        if m <= 0 or r <= 0:
            continue
        
        sum_m += m
        sum_r += r
        sum_m2 += m ** 2
        sum_r2 += r ** 2
    
    n_samples = max(1, n_samples)  # Ensure at least one sample is used to avoid division by zero
    mean_m = Fraction(sum_m, n_samples)
    mean_r = Fraction(sum_r, n_samples)
    
    if n_samples < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n_samples,
            "n_max": max(40, random.randint(5, 40)),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    denominator = math.sqrt((n_samples * sum_m2 - mean_m ** 2) * (n_samples * sum_r2 - mean_r ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n_samples,
            "n_max": max(40, random.randint(5, 40)),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = (n_samples * sum_m * sum_r - sum_m * sum_r) / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_samples,
        "n_max": max(40, random.randint(5, 40)),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")