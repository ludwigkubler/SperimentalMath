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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input length must be a power of 2")
    
    def binary_search(left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        f_left = [f[i] for i in range(2**mid)]
        f_right = [f[i] for i in range(2**mid, 2**(mid+1))]
        
        if all(f_left == f_right):
            return binary_search(left, mid)
        else:
            return 1 + max(binary_search(left, mid), binary_search(mid+1, right))
    
    return binary_search(0, n)

def minimal_tropical_motivic_rank(f):
    # Placeholder for the actual implementation
    # This is a dummy function that returns a constant value
    # You need to implement the actual algorithm here
    return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        mtr_f = minimal_tropical_motivic_rank(f)
        
        if c_f == 0:
            continue
        
        results.append({
            "n": n,
            "c_f": c_f,
            "mtr_f": mtr_f
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["mtr_f"] / r["c_f"] for r in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))**0.5
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": all(0.95 <= x <= 1.05 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_C = sum(r["metric_value"] for r in results) / len(results)
        std_C = (sum((r["metric_value"] - mean_C)**2 for r in results) / len(results))**0.5
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_support")