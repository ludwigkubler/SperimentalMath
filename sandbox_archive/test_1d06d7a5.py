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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(1, n):
            if any(f[j] != f[j ^ (1 << k)] for k in range(i)):
                rank += 1
        return rank ** 2 / n
    
    def alexander_orlik_solomon_invariant(link):
        # Placeholder implementation; actual computation is complex and not provided here
        return random.random()
    
    correlation_coefficient = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):  # Test with 5 instances per size
            f = generate_boolean_function(n)
            rc_f = communication_complexity_rank_variance(f)
            alpha_omega_f = alexander_orlik_solomon_invariant(f)
            correlation_coefficient.append((alpha_omega_f, rc_f))
            instances_tested += 1
    
    if not correlation_coefficient:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    alpha_values, rc_values = zip(*correlation_coefficient)
    mean_alpha = sum(alpha_values) / len(alpha_values)
    mean_rc = sum(rc_values) / len(rc_values)
    covariance = sum((alpha - mean_alpha) * (rc - mean_rc) for alpha, rc in correlation_coefficient) / len(correlation_coefficient)
    variance_alpha = sum((alpha - mean_alpha) ** 2 for alpha in alpha_values) / len(alpha_values)
    variance_rc = sum((rc - mean_rc) ** 2 for rc in rc_values) / len(rc_values)
    correlation_coefficient_value = covariance / (math.sqrt(variance_alpha) * math.sqrt(variance_rc))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient_value >= 0.8 and all(cc >= 0.5 for cc in correlation_coefficient),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data")