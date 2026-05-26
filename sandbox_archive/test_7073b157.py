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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random Boolean function with n variables
        boolean_function = ''.join(random.choice('01') for _ in range(2**n))
        
        # Construct the Tseitin circuit (simplified version)
        tseitin_circuit = boolean_function
        
        # Compute the minimal rank of the quaternionic Kähler manifold
        # This is a placeholder function. Replace with actual computation.
        min_rank = len(tseitin_circuit)  # Simplified for demonstration
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "log_n": math.log(n, 2)
        })
    
    # Calculate the mean and standard deviation of the minimal ranks
    mean_min_rank = sum(result["min_rank"] for result in results) / len(results)
    std_min_rank = math.sqrt(sum((result["min_rank"] - mean_min_rank)**2 for result in results) / len(results))
    
    # Check if the conjecture holds
    support_fraction = sum(1 for result in results if abs(result["min_rank"] - result["log_n"]) <= 0.1 * result["log_n"]) / len(results)
    conjecture_holds = support_fraction >= 0.9
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={results[0]['n']}, min_rank={results[0]['min_rank']}, log_n={results[0]['log_n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, min_rank={results[0]['min_rank']}, log_n={results[0]['log_n']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")