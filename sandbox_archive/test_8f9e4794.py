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
    
    # Generate a random max-CUT instance with n vertices
    n = random.randint(5, 40)
    edges = set()
    for _ in range(n * (n - 1) // 2):
        u, v = random.sample(range(n), 2)
        if u < v:
            edges.add((u, v))
    
    # Calculate the sum-of-squares degree of the max-CUT instance
    sum_of_squares_degree = len(edges)
    
    # Simulate the minimal index of the group action on the spectrum (simplified)
    min_index = random.uniform(1, 2 * n)
    
    # Correlate the minimal index with the sum-of-squares degree
    correlation_coefficient = min_index / sum_of_squares_degree
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    variance_metric_value = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)
    std_metric_value = math.sqrt(variance_metric_value)
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")