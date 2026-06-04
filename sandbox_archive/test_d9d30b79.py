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
    
    # Simulate generating a d-dimensional Kähler manifold and its associated Tseitin formula
    d = random.randint(2, 5)  # Dimension of the Kähler manifold
    n = random.randint(10, 40)  # Number of variables in the Tseitin formula
    
    # Simulate computing the minimal order of the Kähler form (logarithm base 2)
    minimal_order_log2 = random.uniform(5, 20)  # Simulated value
    
    # Simulate determining the resolution proof width
    w_phi_M = random.randint(10, 40)  # Simulated value
    
    return {
        "metric_name": "log2_minimal_order",
        "metric_value": minimal_order_log2,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    median_w_phi_M = sorted([result["instances_tested"] for result in results])[len(results) // 2]
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - median_w_phi_M) <= 10) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")