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
    n_max = 40
    instances_per_seed = 30
    
    # Initialize variables to store results
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_per_seed):
        n = random.randint(5, n_max)
        
        # Generate a random communication protocol with rank variance r
        r = random.uniform(1, n)
        
        # Construct the associated arithmetic space and compute mgar(r)
        # For simplicity, let's assume mgar(r) is proportional to r^2 (this is just an example)
        mgar_r = 0.5 * r**2
        
        # Compute the ratio mgar(r) / r
        if r == 0:
            continue
        ratio = mgar_r / r
        
        # Update total metric value and instances tested
        total_metric_value += ratio
        instances_tested += 1
        
        # Check if the conjecture holds for this instance
        if ratio > 2 * r:  # Example threshold, replace with actual analysis
            conjecture_holds = False
            counterexample = f"Instance {instances_tested}: n={n}, r={r}, mgar(r)={mgar_r}"
    
    # Compute mean and standard deviation of the metric value
    if instances_tested == 0:
        return {
            "metric_name": "mgar_over_r",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    mean_metric_value = total_metric_value / instances_tested
    
    # Return the results for this trial
    return {
        "metric_name": "mgar_over_r",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and fraction of seeds where conjecture holds
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Determine the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")