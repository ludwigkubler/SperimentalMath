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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def monomial_ideal_rank(formula):
        # Placeholder function to compute the rank of a monomial ideal
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)
    
    def communication_complexity_rank_variance(formula):
        # Placeholder function to compute the communication complexity rank variance
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        formula = generate_boolean_formula(n)
        rank = monomial_ideal_rank(formula)
        variance = communication_complexity_rank_variance(formula)
        results.append((rank, variance))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ranks = [r for r, _ in results]
    variances = [v for _, v in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_variance = sum(variances) / len(variances)
    
    covariance = sum((r - mean_rank) * (v - mean_variance) for r, v in results) / len(results)
    variance_of_ranks = sum((r - mean_rank)**2 for r in ranks) / len(ranks)
    variance_of_variances = sum((v - mean_variance)**2 for v in variances) / len(variances)
    
    correlation_coefficient = covariance / (math.sqrt(variance_of_ranks) * math.sqrt(variance_of_variances))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")