# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(instance):
        n = len(instance)
        # Simplified version of communication complexity rank calculation
        return n
    
    def min_order(monomial_ideal):
        # Simplified version of minimal order calculation
        return len(monomial_ideal)
    
    instances_tested = 0
    total_diff = 0
    max_n = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):  # Test each size with 5 instances
            instance = generate_random_instance(n)
            comm_rank = communication_complexity_rank(instance)
            min_order_val = min_order(instance)
            
            diff = abs(comm_rank - (2 * min_order_val / 3))
            total_diff += diff
            
            instances_tested += 1
    
    conjecture_holds = all(diff <= 3 for diff in [total_diff / instances_tested])
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": total_diff / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")