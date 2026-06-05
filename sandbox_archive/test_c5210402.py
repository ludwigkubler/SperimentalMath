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
    
    # Generate a random boolean function with n variables and m clauses
    n = 5 + (seed % 6) * 5  # Sweep n through {5, 10, 15, 20, 30, 40}
    m = int(2 ** (n - 1))  # Ensure a diverse set of functions
    boolean_function = [random.choice([True, False]) for _ in range(m)]
    
    # Compute the Shannon entropy of the boolean function
    entropy = 0.0
    for value in boolean_function:
        if value:
            entropy -= (1 / m) * math.log2(1 / m)
        else:
            entropy -= (1 / m) * math.log2(1 / m)
    
    # Compute the minimal geometric flow order (simplified example)
    # This is a placeholder for the actual computation
    geometric_flow_order = n  # Simplified linear relationship
    
    # Check if the ratio of geometric flow order to entropy is within a constant factor
    C = 2.0  # Example constant factor
    ratio = geometric_flow_order / entropy
    
    conjecture_holds = abs(ratio - C) <= 1e-6
    counterexample = "" if conjecture_holds else f"GF(f)/H(f) = {ratio}, expected ≈ {C}"
    
    return {
        "metric_name": "GF(f)/H(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"GF(f)/H(f) out of expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")