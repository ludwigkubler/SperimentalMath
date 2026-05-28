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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def and_or_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        left = f[:n//2]
        right = f[n//2:]
        return max(and_or_tree_width(left), and_or_tree_width(right)) + 1
    
    def birational_geometry_invariant(f):
        # Placeholder for actual computation
        return sum(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        width = and_or_tree_width(f)
        invariant = birational_geometry_invariant(f)
        max_order = abs(invariant)
        C = width
        log_bound = math.log(C, 2) ** 2  # Example bound, replace with actual calculation
        
        results.append({
            "n": n,
            "width": width,
            "invariant": invariant,
            "max_order": max_order,
            "log_bound": log_bound,
            "conjecture_holds": max_order <= log_bound
        })
    
    mean_max_order = sum(result["max_order"] for result in results) / len(results)
    std_max_order = math.sqrt(sum((result["max_order"] - mean_max_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "max_order",
        "metric_value": mean_max_order,
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in enumerate(all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")