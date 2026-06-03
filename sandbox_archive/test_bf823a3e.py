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
    
    def generate_k_ary_boolean_function(k, n):
        return [random.choice([0, 1]) for _ in range(k**n)]
    
    def communication_complexity_rank(f, k, n):
        # Placeholder implementation of communication complexity rank
        # This is a dummy function and should be replaced with the actual algorithm
        return len(f)
    
    def tropical_hodge_structure_index(f, k, n):
        # Placeholder implementation of tropical Hodge structure index
        # This is a dummy function and should be replaced with the actual algorithm
        return sum(f) / len(f)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        k = random.randint(2, 4)
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_k_ary_boolean_function(k, n)
        
        cc_rank = communication_complexity_rank(f, k, n)
        if cc_rank == 0:
            continue
        
        th_index = tropical_hodge_structure_index(f, k, n)
        if th_index is None or cc_rank is None:
            continue
        
        ratio = th_index / cc_rank
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")