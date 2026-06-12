# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_minimal_order(solutions):
        n = len(solutions[0])
        if not solutions:
            return None
        
        order = 1
        while True:
            found = False
            for s in solutions:
                if any(all(s[j] == s[k] for j, k in combinations(range(n), i)) for i in range(1, n)):
                    found = True
                    break
            if not found:
                return order
            order += 1
    
    def resolution_width(instance):
        # Placeholder function to compute resolution width
        # This is a dummy implementation and should be replaced with actual logic
        return len(instance)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_order = 0
        max_order = 0
        
        for _ in range(30):
            instance = generate_boolean_instance(n)
            solutions = [instance]
            order = compute_minimal_order(solutions)
            if order is None:
                continue
            
            width = resolution_width(instance)
            results.append((order, width))
            
            instances_tested += 1
            max_order = max(max_order, order)
        
        if instances_tested < 30:
            return {
                "metric_name": "minimal_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max_order,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_order = sum(order for order, _ in results) / len(results)
        mean_width = sum(width for _, width in results) / len(results)
        error = abs(mean_order - n ** (1/3)) / (n ** (1/3))
        
        if error < 0.1:
            conjecture_holds = True
        else:
            conjecture_holds = False
        
        return {
            "metric_name": "minimal_order",
            "metric_value": mean_order,
            "instances_tested": instances_tested,
            "n_max": max_order,
            "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")