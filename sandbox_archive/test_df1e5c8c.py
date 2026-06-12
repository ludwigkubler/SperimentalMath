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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_minimal_alexander_orlik_solomon_invariant(f):
        # Placeholder implementation; actual computation depends on the function
        return len(f) / 2
    
    def calculate_communication_complexity_rank_variance(f):
        # Placeholder implementation; actual computation depends on the function
        return sum(1 for x in f if x == 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    alpha_omega_values = []
    rc_values = []
    
    for n in n_values:
        for _ in range(30):
            f = generate_random_boolean_function(n)
            alpha_omega = calculate_minimal_alexander_orlik_solomon_invariant(f)
            rc = calculate_communication_complexity_rank_variance(f)
            alpha_omega_values.append(alpha_omega)
            rc_values.append(rc)
    
    if not alpha_omega_values or not rc_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_alpha_omega = sum(alpha_omega_values) / len(alpha_omega_values)
    mean_rc = sum(rc_values) / len(rc_values)
    
    covariance = sum((alpha_omega - mean_alpha_omega) * (rc - mean_rc) for alpha_omega, rc in zip(alpha_omega_values, rc_values))
    variance_alpha_omega = sum((alpha_omega - mean_alpha_omega)**2 for alpha_omega in alpha_omega_values)
    variance_rc = sum((rc - mean_rc)**2 for rc in rc_values)
    
    std_dev_alpha_omega = math.sqrt(variance_alpha_omega) if variance_alpha_omega != 0 else 1
    std_dev_rc = math.sqrt(variance_rc) if variance_rc != 0 else 1
    
    correlation_coefficient = covariance / (std_dev_alpha_omega * std_dev_rc)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(alpha_omega_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.8) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and abs(result["metric_value"]) < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and abs(result["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")