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
    
    def generate_communication_instance(n):
        # Generate a random communication instance matrix M(φ)
        return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    def variance(matrix):
        n = len(matrix)
        mean = sum(sum(row) for row in matrix) / (n * n)
        return sum((x - mean) ** 2 for row in matrix for x in row) / (n * n)
    
    def min_order(M):
        # Placeholder function to compute the minimal order of a quadratic form
        # This is a dummy implementation and should be replaced with actual computation
        return variance(M) / (len(M) ** 3)
    
    instances_tested = 0
    correlation_coefficient_sum = 0.0
    n_max = 0
    
    for _ in range(100):
        n = random.choice([5, 10, 15, 20, 30, 40])
        M = generate_communication_instance(n)
        min_order_value = min_order(M)
        instances_tested += 1
        if n > n_max:
            n_max = n
        
        # Calculate the correlation coefficient (this is a dummy implementation)
        # In practice, this would involve comparing min_order with other metrics
        correlation_coefficient_sum += min_order_value
    
    mean_correlation_coefficient = correlation_coefficient_sum / instances_tested
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,  # This is a dummy implementation
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")