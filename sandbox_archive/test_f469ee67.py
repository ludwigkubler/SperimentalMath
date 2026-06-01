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
    
    def generate_instance(n):
        # Generate a random instance of size n
        return [random.randint(0, 100) for _ in range(n)]
    
    def compute_local_ring_norm(instance):
        # Compute the minimal norm of the local ring extension
        norm = sum(x**2 for x in instance)
        return math.sqrt(norm)
    
    def compute_growth_rate(instance):
        # Compute the growth rate of communication complexity
        n = len(instance)
        return n * (n + 1) // 2
    
    def pearson_correlation_coefficient(x, y):
        # Compute the Pearson correlation coefficient
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    def theta_bound(n):
        # Define the Θ(f(n)) bound
        return n**2
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_instance(n)
        norm = compute_local_ring_norm(instance)
        growth_rate = compute_growth_rate(instance)
        results.append((norm, growth_rate))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    norms, growth_rates = zip(*results)
    corr_coeff = pearson_correlation_coefficient(norms, growth_rates)
    upper_bound = theta_bound(n_max)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": corr_coeff >= 0.8 and upper_bound <= theta_bound(n_max),
        "counterexample": "" if corr_coeff >= 0.8 and upper_bound <= theta_bound(n_max) else f"corr_coeff={corr_coeff}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        std_corr_coeff = math.sqrt(sum((result["metric_value"] - mean_corr_coeff)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")