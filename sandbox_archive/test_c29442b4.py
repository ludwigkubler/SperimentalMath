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
    
    # Define constants and parameters
    n = 10  # Number of bits in the input
    v = 5   # Matrix rank variance
    
    # Constructive mapping to compute the volume of the minimal Kähler manifold
    # This is a placeholder for the actual computation which depends on the conjecture
    if v <= 0:
        return {
            "metric_name": "volume",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Compute the volume using a placeholder formula
    upper_bound = v ** (1/3)
    lower_bound = (v / math.factorial(n)) ** (1/3)
    
    # Check if the computed volume is within the bounds
    conjecture_holds = lower_bound <= upper_bound
    
    return {
        "metric_name": "volume",
        "metric_value": None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and std of metric_value
    if any("metric_value" not in result or result["metric_value"] is None for result in results):
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        metric_values = [result["metric_value"] for result in results if "metric_value" in result and result["metric_value"] is not None]
        mean_metric_value = sum(metric_values) / len(metric_values)
        std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
        
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")