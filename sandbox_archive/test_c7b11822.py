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
    
    def generate_instance(n):
        # Generate a random communication complexity instance with rank variance r
        r = random.randint(1, n // 2)
        return r
    
    def minimal_representation_length(r, n):
        # Simulate the minimal representation length using geometric representation theory
        mrep = 2 * r * math.log(n, 2)  # Simplified model for demonstration
        return mrep
    
    n_values = [5, 10, 15, 20, 30, 40]
    r_values = []
    mrep_values = []
    
    for n in n_values:
        instances_tested = 30
        for _ in range(instances_tested):
            r = generate_instance(n)
            mrep = minimal_representation_length(r, n)
            r_values.append(r)
            mrep_values.append(mrep)
    
    mean_r = sum(r_values) / len(r_values)
    mean_mrep = sum(mrep_values) / len(mrep_values)
    
    if len(r_values) == 0 or len(mrep_values) == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    numerator = sum((r - mean_r) * (mrep - mean_mrep) for r, mrep in zip(r_values, mrep_values))
    denominator = len(r_values) * math.sqrt(sum((r - mean_r)**2 for r in r_values)) * math.sqrt(sum((mrep - mean_mrep)**2 for mrep in mrep_values))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient > 0.8 and all(mrep <= 1.5 * r for r, mrep in zip(r_values, mrep_values))
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_threshold_not_met" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_threshold_not_met' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")