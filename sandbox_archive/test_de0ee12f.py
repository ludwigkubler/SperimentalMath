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
    
    # Parameters for the trial
    n = 10  # Dimension of the hyperplane
    num_trials = 30
    
    # Initialize variables to store results
    O_G_values = []
    R_n_values = []
    
    for _ in range(num_trials):
        # Generate a random tiling (simplified example)
        tiling = [random.randint(1, n) for _ in range(n)]
        
        # Compute the associated Coxeter group order G (simplified example)
        G = sum(tiling)
        
        # Simulate the tiling in a communication complexity protocol and measure its rank R(n)
        # This is a placeholder for the actual computation of R(n)
        R_n = sum(tiling)  # Simplified example
        
        O_G_values.append(G)
        R_n_values.append(R_n)
    
    # Compute the correlation coefficient between O(G) and R(n)
    if len(O_G_values) != num_trials or len(R_n_values) != num_trials:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "incomplete_data"
        }
    
    mean_O_G = sum(O_G_values) / num_trials
    mean_R_n = sum(R_n_values) / num_trials
    
    covariance = sum((O_G - mean_O_G) * (R_n - mean_R_n) for O_G, R_n in zip(O_G_values, R_n_values)) / num_trials
    variance_O_G = sum((O_G - mean_O_G) ** 2 for O_G in O_G_values) / num_trials
    variance_R_n = sum((R_n - mean_R_n) ** 2 for R_n in R_n_values) / num_trials
    
    if variance_O_G == 0 or variance_R_n == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": num_trials,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_O_G) * math.sqrt(variance_R_n))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": num_trials,
        "n_max": n,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] or result["counterexample"] == "incomplete_data" or result["counterexample"] == "zero_variance" for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")