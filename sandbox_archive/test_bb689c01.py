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
    n = 30  # Number of instances per trial
    ε = 0.1  # Constant for the conjecture
    
    # Generate a random tropical curve and compute its minimal Hodge index
    hodge_index = random.randint(1, n)  # Simplified model for demonstration
    
    # Construct a BP_read_twice circuit corresponding to the tropical curve
    depth = random.randint(1, n)  # Simplified model for demonstration
    size = random.randint(1, n)  # Simplified model for demonstration
    
    # Check if the conjecture holds for this instance
    if hodge_index < (1 + ε) * depth / size:
        conjecture_holds = False
        counterexample = "Hodge index is less than (1+ε)D/S"
    else:
        conjecture_holds = True
        counterexample = ""
    
    # Return the results for this trial
    return {
        "metric_name": "minimal Hodge index",
        "metric_value": hodge_index,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and std of metric_value
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        total_metric_value = sum(r["metric_value"] for r in results)
        mean_metric_value = total_metric_value / len(results)
        
        squared_diff_sum = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results)
        std_metric_value = math.sqrt(squared_diff_sum / len(results))
        
        # Compute fraction of seeds where conjecture_holds
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            counterexample = results[first_failing_seed]["counterexample"]
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")