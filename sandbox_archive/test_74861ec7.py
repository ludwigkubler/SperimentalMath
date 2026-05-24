# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define constants and parameters
    n = 10  # Number of qubits (can vary between trials)
    c_K = 2 * n  # Example constant for function field K
    
    # Generate a random Kähler manifold rank r(M)
    r_M = random.randint(1, 5)  # Simplified for testing purposes
    
    # Calculate the quantum query complexity Q(Bell, n)
    Q_Bell_n = c_K * r_M / n
    
    # Check if the conjecture holds
    conjecture_holds = (Q_Bell_n >= c_K)
    
    # Return the trial results
    return {
        "metric_name": "quantum_query_complexity",
        "metric_value": Q_Bell_n,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"r(M) = {r_M} < c(K)/n = {c_K}/{n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    
    squared_diff_sum = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)
    std_metric_value = (squared_diff_sum / len(results)) ** 0.5
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    # Determine the final result
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < c(K)/n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")