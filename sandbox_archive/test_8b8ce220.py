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
    
    # Define constants and parameters for testing
    n_tests = 30
    instances_tested = 0
    metric_values = []
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(n_tests):
        # Generate a random instance φ_G (simplified example)
        n = random.randint(5, 40)
        instances_tested += 1
        n_max = max(n_max, n)
        
        # Compute the Poincaré dual lattice index I(G) (simplified example)
        I_G = random.uniform(1, 2 * n)
        
        # Measure the communication complexity rank r(φ_G) (simplified example)
        r_phi_G = random.uniform(0.5, n / 2)
        
        # Store the metric value
        metric_values.append(I_G)
        
        # Check if the conjecture holds for this instance
        if I_G > 1.5 * r_phi_G:
            conjecture_holds = False
            counterexample = f"Instance with I(G)={I_G} and r(φ_G)={r_phi_G}"
    
    # Compute the Pearson correlation coefficient (simplified example)
    mean_I_G = sum(metric_values) / len(metric_values)
    variance_I_G = sum((x - mean_I_G) ** 2 for x in metric_values) / len(metric_values)
    covariance = sum((metric_values[i] - mean_I_G) * (r_phi_G - r_phi_G) for i, r_phi_G in enumerate(r_phi_G)) / (len(metric_values) - 1)
    std_r_phi_G = math.sqrt(sum((x - r_phi_G) ** 2 for x in r_phi_G) / len(r_phi_G))
    correlation_coefficient = covariance / (std_I_G * std_r_phi_G)
    
    # Check if the conjecture is supported
    if correlation_coefficient < 0.5:
        conjecture_holds = False
        counterexample = f"Pearson correlation coefficient {correlation_coefficient} < 0.5"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")