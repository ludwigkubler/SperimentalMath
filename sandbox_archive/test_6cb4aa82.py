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
    
    # Define the communication protocol
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 10))
    inputs = [random.sample(range(1, n+1), n) for _ in range(k)]
    protocol = (inputs,)

    # Compute the minimal symplectic volume
    # This is a placeholder function. Replace it with actual computation.
    def compute_symplectic_volume(protocol):
        # Placeholder implementation
        return random.random()

    min_vol = compute_symplectic_volume(protocol)
    
    # Measure the communication complexity
    def compute_communication_complexity(protocol):
        # Placeholder implementation
        return random.randint(1, n)

    comm_complexity = compute_communication_complexity(protocol)
    
    # Check if the conjecture holds
    conjecture_holds = min_vol > 0.5 * comm_complexity and min_vol <= 0.2 * comm_complexity
    
    # Return the result
    return {
        "metric_name": "symplectic_volume",
        "metric_value": min_vol,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "mapping_undefined" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    # Compute mean and standard deviation of metric_value
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        total_metric_value = sum(r["metric_value"] for r in results)
        mean_metric_value = total_metric_value / len(results)
        variance = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)
        std_deviation = math.sqrt(variance)

        # Compute the fraction of seeds where conjecture_holds
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

        # Determine if the conjecture is supported
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no_results")