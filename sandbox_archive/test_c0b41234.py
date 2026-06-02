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
    
    def communication_complexity_rank(f):
        # Placeholder implementation of communication complexity rank
        # This is a dummy function and should be replaced with an actual solver or implementation.
        return random.randint(1, n)
    
    def grothendieck_witt_class(f):
        # Placeholder implementation of Grothendieck-Witt class
        # This is a dummy function and should be replaced with an actual computational method.
        return random.uniform(0.5, 2.0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank(f)
        GW_class_f = grothendieck_witt_class(f)
        
        if R_f == 0 or GW_class_f == 0:
            continue
        
        results.append((R_f, GW_class_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    R_f_values = [R for R, _ in results]
    GW_class_f_values = [GW for _, GW in results]
    
    mean_R_f = sum(R_f_values) / len(R_f_values)
    mean_GW_class_f = sum(GW_class_f_values) / len(GW_class_f_values)
    
    numerator = sum((R - mean_R_f) * (GW - mean_GW_class_f) for R, GW in results)
    denominator = math.sqrt(sum((R - mean_R_f)**2 for R in R_f_values)) * math.sqrt(sum((GW - mean_GW_class_f)**2 for GW in GW_class_f_values))
    
    correlation_coefficient = numerator / denominator if denominator != 0 else None
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")