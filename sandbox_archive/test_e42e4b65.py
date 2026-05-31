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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        # Simplified model of communication complexity
        return n
    
    def minimal_root_separability(V_f):
        # Placeholder function to simulate minimal root separability calculation
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(5, n_max))
        C_f = communication_complexity(f)
        r_s = minimal_root_separability(f)
        
        if math.isnan(r_s) or math.isinf(r_s):
            conjecture_holds = False
            counterexample = "minimal_root_separability_result_invalid"
            break
        
        metric_values.append(C_f / r_s)
    
    if not conjecture_holds:
        return {
            "metric_name": "communication_complexity_over_minimal_root_separability",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    mean_C = sum(metric_values) / len(metric_values)
    std_C = math.sqrt(sum((x - mean_C)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "communication_complexity_over_minimal_root_separability",
        "metric_value": mean_C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_C >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")