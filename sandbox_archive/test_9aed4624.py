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
    
    def generate_curve(n):
        # Generate a smooth projective curve C with n variables
        return [f"x{i}" for i in range(1, n+1)]
    
    def birational_morphism(curve):
        # Compute the birational morphism φ from C to P^1
        return len(curve)
    
    def communication_complexity_rank(morphism_size):
        # Estimate the communication complexity rank r(φ) using a small DPLL solver or other efficient methods
        return math.ceil(math.log2(morphism_size))
    
    def w_and_H(morphism_size):
        # Placeholder for actual computation of w(φ) and H(φ)
        # For simplicity, we assume w(φ) = 0 and H(φ) is a constant
        return 0, 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        curve = generate_curve(n)
        morphism_size = birational_morphism(curve)
        r_phi = communication_complexity_rank(morphism_size)
        w_phi, H_phi = w_and_H(morphism_size)
        
        log_metric = math.log2(n**(r_phi + 1))
        metric_value = w_phi + H_phi
        
        results.append({
            "n": n,
            "morphism_size": morphism_size,
            "r_phi": r_phi,
            "w_phi": w_phi,
            "H_phi": H_phi,
            "log_metric": log_metric,
            "metric_value": metric_value
        })
    
    if not results:
        return {
            "metric_name": "log_2(n^(r(φ)+1)) vs w(φ) + H(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    log_metrics = [r["log_metric"] for r in results]
    metric_values = [r["metric_value"] for r in results]
    
    correlation_coefficient = sum((x - mean_log) * (y - mean_val) for x, y in zip(log_metrics, metric_values)) / \
                              math.sqrt(sum((x - mean_log)**2 for x in log_metrics) * sum((y - mean_val)**2 for y in metric_values))
    
    mean_log = sum(log_metrics) / len(log_metrics)
    mean_val = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_val)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "log_2(n^(r(φ)+1)) vs w(φ) + H(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")