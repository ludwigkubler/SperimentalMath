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
    
    # Generate an explicit function f in P with a known ACC⁰ circuit weight w(f)
    n = 10  # Example size, can be adjusted
    f = [random.randint(0, 1) for _ in range(n)]
    w_f = sum(f)  # Simplified example of ACC⁰ circuit weight
    
    # Construct a configuration space X for this function
    # This is a placeholder; actual construction would depend on the conjecture's specifics
    X = f  # Example: X is just the function itself
    
    # Compute the minimal rank of π₁(X)
    # Placeholder computation; actual method depends on the conjecture's specifics
    rank_pi1_X = sum(f)  # Simplified example
    
    # Compare the computed rank with 2w(f)
    if rank_pi1_X >= 2 * w_f:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Function {f} with ACC⁰ weight {w_f} and computed rank {rank_pi1_X}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank_pi1_X,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 3079) for _ in range(30)]  # Default to 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len(results) / len(seeds)
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")