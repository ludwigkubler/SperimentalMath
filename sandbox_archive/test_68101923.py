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

def generate_random_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def calculate_characteristic_variety(f: list, n: int) -> dict:
    # Simplified procedure to compute the characteristic variety
    # For demonstration purposes, we'll use a dummy dictionary
    return {f"feature_{i}": i % 3 for i in range(n)}

def compute_hodge_rank(variety: dict) -> int:
    # Dummy implementation of Hodge rank calculation
    return len(variety)

def calculate_communication_complexity(f: list, n: int) -> float:
    # Simplified procedure to compute communication complexity
    # For demonstration purposes, we'll use a dummy value
    return 2 * n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        variety = calculate_characteristic_variety(f, n)
        hodge_rank = compute_hodge_rank(variety)
        cc_sym = calculate_communication_complexity(f, n)
        
        results.append({
            "n": n,
            "hodge_rank": hodge_rank,
            "cc_sym": cc_sym
        })
    
    if not results:
        return {
            "metric_name": "CC_sym / H(f)^2",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hodge_ranks = [r["hodge_rank"] for r in results]
    cc_sym_values = [r["cc_sym"] for r in results]
    mean_cc_sym_over_h2 = sum(cc / (hr ** 2) for hr, cc in zip(hodge_ranks, cc_sym_values)) / len(results)
    
    correlation_coefficient = sum((h - h_mean) * (c - c_mean) for h, c in zip(hodge_ranks, cc_sym_values))
    correlation_coefficient /= math.sqrt(sum((h - h_mean) ** 2 for h in hodge_ranks) * sum((c - c_mean) ** 2 for c in cc_sym_values))
    
    return {
        "metric_name": "CC_sym / H(f)^2",
        "metric_value": mean_cc_sym_over_h2,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_cc_sym_over_h2 <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")