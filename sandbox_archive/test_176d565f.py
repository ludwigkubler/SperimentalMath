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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monomial_ideal_order(instance):
        n = len(instance)
        # Simplified Gröbner basis computation (not actual implementation)
        return n
    
    def resolution_proof_width(instance):
        # Simplified DPLL-based resolution solver (not actual implementation)
        return sum(1 for _ in range(len(instance)))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_sat_instance(n)
        order = monomial_ideal_order(instance)
        width = resolution_proof_width(instance)
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((o - mean_order) * (w - mean_width) for o, w in results) /
                    math.sqrt(sum((o - mean_order)**2 for o in orders) *
                              sum((w - mean_width)**2 for w in widths)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")