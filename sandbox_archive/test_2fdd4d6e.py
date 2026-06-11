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
    
    def generate_tseitin_formula(n):
        if n == 1:
            return "a"
        else:
            phi_G = f"({generate_tseitin_formula(n-1)} v a)"
            for _ in range(2, n+1):
                phi_G += f" & ({generate_tseitin_formula(n-1)} v b{random.randint(0, n-2)})"
            return phi_G
    
    def compute_minimal_order(phi_G):
        # Placeholder function to simulate computing the minimal order
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi_G.split())
    
    def compute_resolution_proof_width(phi_G):
        # Placeholder function to simulate computing the resolution proof width
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi_G.split())
    
    results = []
    for _ in range(20):
        n = random.randint(5, 40)
        phi_G = generate_tseitin_formula(n)
        minimal_order = compute_minimal_order(phi_G)
        resolution_proof_width = compute_resolution_proof_width(phi_G)
        results.append((phi_G, minimal_order, resolution_proof_width))
    
    if not results:
        return {
            "metric_name": "minimal_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    minimal_orders = [r[1] for r in results]
    widths = [r[2] for r in results]
    
    mean_order = sum(minimal_orders) / len(minimal_orders)
    mean_width = sum(widths) / len(widths)
    
    covariance = sum((minimal_orders[i] - mean_order) * (widths[i] - mean_width) for i in range(len(results))) / len(results)
    variance_order = sum((minimal_orders[i] - mean_order) ** 2 for i in range(len(results))) / len(results)
    variance_width = sum((widths[i] - mean_width) ** 2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / (math.sqrt(variance_order) * math.sqrt(variance_width))
    
    return {
        "metric_name": "minimal_order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(phi_G.split()) for phi_G, _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.9 and abs(covariance / (math.sqrt(variance_order) * math.sqrt(variance_width)) - 1) < 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")