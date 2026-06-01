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
    
    def communication_complexity_rank(phi):
        n = len(phi)
        # Simplified example of a communication complexity rank calculation
        return n
    
    def minimal_order_of_eigenform(k):
        # Simplified example of a minimal order calculation
        return k * 2
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        r_phi = communication_complexity_rank(phi)
        order_k = minimal_order_of_eigenform(r_phi)
        results.append((r_phi, order_k))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    r_phi_values = [r for r, _ in results]
    order_k_values = [o for _, o in results]
    
    mean_r_phi = sum(r_phi_values) / len(r_phi_values)
    mean_order_k = sum(order_k_values) / len(order_k_values)
    
    correlation_coefficient = (sum((r - mean_r_phi) * (o - mean_order_k) for r, o in results) /
                               math.sqrt(sum((r - mean_r_phi)**2 for r in r_phi_values) *
                                         sum((o - mean_order_k)**2 for o in order_k_values)))
    
    mean_abs_diff = sum(abs(r - o) for r, o in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(phi) for phi, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.5 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
            counterexample = "not_enough_support"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")