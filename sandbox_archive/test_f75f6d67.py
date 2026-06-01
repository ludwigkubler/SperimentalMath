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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        # Placeholder function to compute the communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def minimal_order_of_eigenform(k):
        # Placeholder function to compute the minimal order of an eigenform
        # This is a dummy implementation and should be replaced with actual logic
        return k
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        r_phi = communication_complexity_rank(phi)
        order_k = minimal_order_of_eigenform(r_phi)
        
        if order_k == 0 or r_phi == 0:
            continue
        
        correlation = abs(order_k - r_phi) / max(order_k, r_phi)
        results.append({
            "n": n,
            "r_phi": r_phi,
            "order_k": order_k,
            "correlation": correlation
        })
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_correlation = sum(result["correlation"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    return {
        "metric_name": "Correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": all(result["correlation"] >= 0.5 for result in results) and mean_correlation <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")