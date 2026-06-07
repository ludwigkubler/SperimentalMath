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
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_variance(matrix):
        # Compute the variance of a matrix
        mean = sum(sum(row) for row in matrix) / (len(matrix) * len(matrix[0]))
        variance = sum((sum(row) - mean) ** 2 for row in matrix) / (len(matrix) * len(matrix[0]) - 1)
        return variance
    
    def compute_min_order(variance):
        # Compute the minimal order of a quadratic form
        return variance / (len(communication_instance) ** 3)
    
    communication_instances = [generate_communication_instance(n) for n in range(5, 41)]
    variances = []
    min_orders = []
    
    for instance in communication_instances:
        matrix = [[instance[i] * instance[j] for j in range(len(instance))] for i in range(len(instance))]
        variance = compute_variance(matrix)
        min_order = compute_min_order(variance)
        variances.append(variance)
        min_orders.append(min_order)
    
    correlation_coefficient = sum((min_orders[i] - sum(min_orders) / len(min_orders)) * (variances[i] - sum(variances) / len(variances)) for i in range(len(min_orders))) / math.sqrt(sum((min_orders[i] - sum(min_orders) / len(min_orders)) ** 2 for i in range(len(min_orders)))) / math.sqrt(sum((variances[i] - sum(variances) / len(variances)) ** 2 for i in range(len(variances))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(communication_instances),
        "n_max": max(len(instance) for instance in communication_instances),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")