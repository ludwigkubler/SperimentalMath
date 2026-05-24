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
    
    # Define the mapping from tensor network to Kähler class rank
    def kahler_rank(n):
        if n <= 4:
            return n
        else:
            return mapping_undefined
    
    # Generate a random tensor network state of size n
    n = random.randint(5, 40)
    tensor_network_state = [random.randint(0, 1) for _ in range(n)]
    
    # Calculate the quantum query complexity (simplified example)
    q_query_complexity = sum(tensor_network_state)
    
    # Compute the associated Kähler class rank
    kahler_class_rank = kahler_rank(n)
    
    if kahler_class_rank == "mapping_undefined":
        return {
            "metric_name": "kahler_class_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate the correlation coefficient
    correlation_coefficient = Fraction(q_query_complexity, kahler_class_rank).limit_denominator()
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    instances_tested = sum(result["instances_tested"] for result in results)
    mean_metric_value = total_metric_value / instances_tested
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["metric_value"] is not None for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.9' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")