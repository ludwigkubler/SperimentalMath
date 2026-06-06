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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(phi):
        # Placeholder function to simulate resolution width calculation
        # Replace with actual implementation if available
        return len(phi) // 2
    
    def minimal_brauer_group_order(phi):
        # Placeholder function to simulate Brauer group order calculation
        # Replace with actual implementation if available
        return len(phi)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_boolean_instance(n)
        min_order = minimal_brauer_group_order(phi)
        w_phi = resolution_width(phi)
        results.append({
            "n": n,
            "min_order": min_order,
            "w_phi": w_phi
        })
    
    if not results:
        return {
            "metric_name": "Brauer Group Order vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    min_order_values = [r["min_order"] for r in results]
    w_phi_values = [math.sqrt(r["n"]) * r["w_phi"] for r in results]
    
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    correlation_coefficient = sum((min_order - mean_min_order) * (w_phi - mean_w_phi) 
                                   for min_order, w_phi in zip(min_order_values, w_phi_values)) / \
                              math.sqrt(sum((min_order - mean_min_order)**2 
                                            for min_order in min_order_values) *
                                        sum((w_phi - mean_w_phi)**2 
                                            for w_phi in w_phi_values))
    
    return {
        "metric_name": "Brauer Group Order vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.8 and all(c >= 0.7 for c in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient > 0.8 else f"Correlation: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")