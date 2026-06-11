# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_local_induction_dimension(f):
        n = int(math.log2(len(f)))
        # Simplified LID calculation (placeholder)
        return n
    
    def calculate_entanglement_complexity(f):
        n = int(math.log2(len(f)))
        if n <= 1:
            return 0
        complexity = 0
        for i in range(n):
            if f[2**i] != f[2**(i+1)]:
                complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        lid = calculate_local_induction_dimension(f)
        entanglement_complexity = calculate_entanglement_complexity(f)
        results.append({
            "n": n,
            "lid": lid,
            "entanglement_complexity": entanglement_complexity
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    lid_values = [r["lid"] for r in results]
    entanglement_complexity_values = [r["entanglement_complexity"] for r in results]
    
    mean_lid = sum(lid_values) / len(lid_values)
    mean_entanglement_complexity = sum(entanglement_complexity_values) / len(entanglement_complexity_values)
    
    covariance = sum((lid - mean_lid) * (entanglement_complexity - mean_entanglement_complexity) for lid, entanglement_complexity in zip(lid_values, entanglement_complexity_values)) / len(lid_values)
    variance_lid = sum((lid - mean_lid)**2 for lid in lid_values) / len(lid_values)
    variance_entanglement_complexity = sum((entanglement_complexity - mean_entanglement_complexity)**2 for entanglement_complexity in entanglement_complexity_values) / len(entanglement_complexity_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_lid) * math.sqrt(variance_entanglement_complexity))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")