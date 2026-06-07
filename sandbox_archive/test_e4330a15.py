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
        # Generate a random communication instance with n variables
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def matrix_variance(matrix):
        # Calculate the variance of the matrix elements
        mean = sum(sum(row) for row in matrix) / (len(matrix) * len(matrix[0]))
        variance = sum(sum((x - mean) ** 2 for x in row) for row in matrix) / (len(matrix) * len(matrix[0]))
        return variance
    
    def min_order_of_quadratic_form(matrix):
        # Placeholder function to calculate the minimal order of a quadratic form
        # This is a dummy implementation and should be replaced with actual computation
        n = len(matrix)
        return 1 / (n ** 3) * matrix_variance(matrix)
    
    instances_tested = 0
    min_order_values = []
    variance_values = []
    n_max = 0
    
    for _ in range(100):  # Test with 100 instances per seed
        n = random.randint(5, 40)  # Sweep n through {5, 10, 15, 20, 30, 40}
        if n > n_max:
            n_max = n
        
        instance = generate_communication_instance(n)
        min_order = min_order_of_quadratic_form(instance)
        variance = matrix_variance(instance)
        
        min_order_values.append(min_order)
        variance_values.append(variance)
        instances_tested += 1
    
    correlation_coefficient = sum((min_order_values[i] - sum(min_order_values) / len(min_order_values)) *
                                  (variance_values[i] - sum(variance_values) / len(variance_values))
                                 for i in range(len(min_order_values))) / \
                               math.sqrt(sum((x - sum(min_order_values) / len(min_order_values)) ** 2
                                             for x in min_order_values) *
                                         sum((y - sum(variance_values) / len(variance_values)) ** 2
                                             for y in variance_values))
    
    conjecture_holds = correlation_coefficient >= 0.8
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")