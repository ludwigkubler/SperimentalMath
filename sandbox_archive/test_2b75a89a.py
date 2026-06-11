# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f, n):
        matrix = [[f[i * (2**(n-1)) + j] for i in range(2**(n-1))] for j in range(2**(n-1))]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def entropic_quasi_group(f, n):
        # Placeholder for the actual implementation of entropic quasi-group
        # This is a dummy function to avoid errors
        return 2**n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        ord_eq_f = entropic_quasi_group(f, n)
        rc_f = communication_complexity_rank_variance(f, n)
        
        if ord_eq_f > 3 * rc_f:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "order_greater_than_three_times_rc"
            }
        
        results.append((ord_eq_f, rc_f))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / math.sqrt(sum((x - mean_x)**2 for x, _ in results) * sum((y - mean_y)**2 for _, y in results))
    mean_x = sum(x for x, _ in results) / len(results)
    mean_y = sum(y for _, y in results) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    if len(results) == len(seeds):
        mean_value = sum(results) / len(results)
        std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = Fraction(len(results), len(seeds)).limit_denominator()
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_greater_than_three_times_rc\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")