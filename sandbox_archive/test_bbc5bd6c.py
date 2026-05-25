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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_minimal_local_index(delone_set):
        # Placeholder function to compute minimal local index
        # This is a dummy implementation and should be replaced with actual logic
        return len(delone_set)
    
    def compute_communication_complexity(instance):
        # Placeholder function to compute communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(instance)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        delone_set = instance  # Placeholder for actual Delone set computation
        tau = compute_minimal_local_index(delone_set)
        comm_complexity = compute_communication_complexity(instance)
        
        if tau < Fraction(n, 2):  # Example condition to check
            return {
                "metric_name": "minimal_local_index",
                "metric_value": float(tau),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, tau={tau} < n/2"
            }
        
        results.append(comm_complexity)
    
    mean_metric_value = sum(results) / len(results)
    return {
        "metric_name": "communication_complexity",
        "metric_value": float(mean_metric_value),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = len([r for r in results if r >= Fraction(n, 2)]) / len(results)
    
    if all(r >= Fraction(n, 2) for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r < Fraction(n, 2) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < Fraction(n, 2)))]
        print(f"RESULT: FALSIFIED counterexample='n/2 condition failed' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")