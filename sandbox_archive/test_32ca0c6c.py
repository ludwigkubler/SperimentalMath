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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def arithmetic_hierarchy_complexity(f):
        # Placeholder implementation; actual AH complexity calculation is complex
        return len(f)
    
    def circuit_monotone_width(f):
        # Placeholder implementation; actual monotone width calculation is complex
        return sum(f)
    
    n_values = [30, 35, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        ah_f = arithmetic_hierarchy_complexity(f)
        w_mon_f = circuit_monotone_width(f)
        results.append((ah_f, w_mon_f))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ah_values = [r[0] for r in results]
    w_mon_values = [r[1] for r in results]
    
    mean_ah = sum(ah_values) / len(ah_values)
    mean_w_mon = sum(w_mon_values) / len(w_mon_values)
    
    covariance = sum((ah - mean_ah) * (w_mon - mean_w_mon) for ah, w_mon in results) / len(results)
    variance_ah = sum((ah - mean_ah)**2 for ah in ah_values) / len(ah_values)
    variance_w_mon = sum((w_mon - mean_w_mon)**2 for w_mon in w_mon_values) / len(w_mon_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_ah) * math.sqrt(variance_w_mon))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")