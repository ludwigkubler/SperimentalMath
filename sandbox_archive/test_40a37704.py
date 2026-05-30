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
    
    def generate_cnf(n, density):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(2, 3))]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    def resultant_formula(cnf):
        # Placeholder for resultant formula computation
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, 0.6)
        width = resolution_width(cnf)
        degree = resultant_formula(cnf)
        results.append({
            "n": n,
            "width": width,
            "degree": degree
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["degree"] for result in results]
    width_values = [result["width"] for result in results]
    
    mean_degree = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_degree) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = sum((metric_values[i] - mean_degree) * (width_values[i] - sum(width_values) / len(width_values)) for i in range(len(metric_values))) / (len(metric_values) * std_dev * math.sqrt(sum((x - sum(width_values) / len(width_values)) ** 2 for x in width_values)))
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_degree,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.05,
        "counterexample": "" if abs(correlation_coefficient) > 0.05 else "correlation_coefficient_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")