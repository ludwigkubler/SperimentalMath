# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        # Placeholder implementation; actual computation depends on the function
        return len(f)
    
    def grothendieck_witt_class(f):
        # Placeholder implementation; actual computation depends on the function
        return sum(f) % 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_gw_class = 0
        total_rank = 0
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            rank = communication_complexity_rank(f)
            gw_class = grothendieck_witt_class(f)
            
            if rank == 0 or gw_class == 0:
                continue
            
            total_gw_class += gw_class
            total_rank += rank
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        
        mean_gw_class = total_gw_class / instances_tested
        mean_rank = total_rank / instances_tested
        correlation_coefficient = (instances_tested * sum(gw_class * rank for gw_class, rank in zip(results, results)) - instances_tested * mean_gw_class * mean_rank) / ((instances_tested - 1) * (sum(gw_class**2 for gw_class in results) - instances_tested * mean_gw_class**2))
        
        results.append(correlation_coefficient)
    
    correlation_coefficient = sum(results) / len(results)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
    
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r < 0.7 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < 0.7))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")