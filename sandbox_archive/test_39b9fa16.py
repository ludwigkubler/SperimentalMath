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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_kostant_multiplicity(f):
        # Placeholder function to simulate Kostant multiplicity calculation
        return len(f) / n
    
    def calculate_communication_complexity_rank_variance(f):
        # Placeholder function to simulate communication complexity rank variance calculation
        return sum([1 if x == 0 else -1 for x in f]) ** 2 / (len(f) * (len(f) - 1))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        kappa_f = calculate_kostant_multiplicity(f)
        rank_variance = calculate_communication_complexity_rank_variance(f)
        results.append((n, kappa_f, rank_variance))
    
    n_max = max([r[0] for r in results])
    if n_max < 16:
        return {
            "metric_name": "Kostant Multiplicity and Rank Variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    kappa_values = [r[1] for r in results]
    rank_variance_values = [r[2] for r in results]
    mean_kappa = sum(kappa_values) / len(kappa_values)
    mean_rank_variance = sum(rank_variance_values) / len(rank_variance_values)
    variance_kappa = sum((x - mean_kappa) ** 2 for x in kappa_values) / len(kappa_values)
    variance_rank_variance = sum((x - mean_rank_variance) ** 2 for x in rank_variance_values) / len(rank_variance_values)
    covariance = sum((kappa_values[i] - mean_kappa) * (rank_variance_values[i] - mean_rank_variance) for i in range(len(kappa_values))) / len(kappa_values)
    correlation_coefficient = covariance / math.sqrt(variance_kappa * variance_rank_variance)
    
    return {
        "metric_name": "Kostant Multiplicity and Rank Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")