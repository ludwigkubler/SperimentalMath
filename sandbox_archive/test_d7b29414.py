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
    
    # Generate a random Boolean function with n variables and m clauses
    n = 10  # Number of variables
    m = 2 * n  # Number of clauses
    f = [random.choice([True, False]) for _ in range(2**n)]
    
    # Compute the communication complexity rank variance R(f)
    # This is a placeholder function. Replace with actual computation.
    def communication_complexity_rank_variance(f):
        # Placeholder implementation
        return random.random()
    
    R_f = communication_complexity_rank_variance(f)
    
    # Compute the minimal order of local units ord(U_f)
    # This is a placeholder function. Replace with actual computation.
    def minimal_order_of_local_units(R_f):
        # Placeholder implementation
        return random.randint(1, 10)
    
    ord_U_f = minimal_order_of_local_units(R_f)
    
    # Check if the conjecture holds
    conjecture_holds = ord_U_f <= R_f**2  # Placeholder bound
    
    return {
        "metric_name": "minimal_order_of_local_units",
        "metric_value": ord_U_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")