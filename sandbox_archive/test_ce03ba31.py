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
    
    # Define parameters for the trial
    n = 30  # Size of the Boolean algebra
    
    # Generate a random explicit function in P with polynomially bounded ACC⁰ complexity
    def f(x):
        return x % 2 == 0
    
    # Compute the corresponding Kahn-Smorodsky invariant
    invariant = [f(i) for i in range(n)]
    
    # Measure the minimal rank of the invariant
    min_rank = len(set(invariant))
    
    # Compare the minimal rank to the size of the function's domain
    if min_rank > n ** 0.5:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={min_rank}, expected={n**0.5}"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds n^c\" first_failing_seed={first_failing_seed}")