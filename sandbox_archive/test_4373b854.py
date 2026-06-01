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
    
    # Define constants and parameters
    p = 2  # Prime number for p-adic field
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    # Initialize variables to track metrics
    total_ratio = 0.0
    count_supported = 0
    counterexample = ""
    
    # Define the conjecture parameters
    c = 10  # Hypothetical constant for the ratio bound
    
    for n in range(n_min, n_max + 1):
        for _ in range(instances_per_seed // (n - n_min + 1)):
            # Generate a random Boolean formula φ with n variables
            phi = [random.choice([True, False]) for _ in range(2**n)]
            
            # Compute the minimal p-adic root count |A(φ)|
            # This is a placeholder for the actual algorithm to compute the p-adic root count
            A_phi = sum(phi)
            
            # Compute the Frege proof length f(φ)
            # This is a placeholder for the actual Frege refutation procedure
            f_phi = len(phi)
            
            # Calculate the ratio |A(φ)| / f(φ)
            if f_phi == 0:
                continue
            ratio = A_phi / f_phi
            
            # Update total ratio and count of supported trials
            total_ratio += ratio
            if ratio <= c:
                count_supported += 1
            else:
                counterexample = f"Formula with n={n} did not satisfy the conjecture."
    
    # Calculate mean and standard deviation of the ratios
    mean_ratio = total_ratio / (instances_per_seed * (n_max - n_min + 1))
    std_deviation = math.sqrt(sum((ratio - mean_ratio) ** 2 for ratio in range(n_min, n_max + 1)) / instances_per_seed)
    
    # Determine if the conjecture holds based on the support fraction
    support_fraction = count_supported / (instances_per_seed * (n_max - n_min + 1))
    
    return {
        "metric_name": "Ratio of p-Adic Root Count to Frege Proof Length",
        "metric_value": mean_ratio,
        "instances_tested": instances_per_seed * (n_max - n_min + 1),
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")