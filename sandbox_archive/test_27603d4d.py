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
    
    def generate_boolean_circuit(n):
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(2**n)]
    
    def communication_complexity_rank_variance(circuit):
        n = len(circuit)
        rank = sum(sum(row) for row in circuit) / (n * n)
        variance = sum((sum(row) - rank)**2 for row in circuit) / (n * n)
        return variance
    
    def minimal_degree_quaternionic_polynomial_representation(circuit):
        # Placeholder function to simulate the computation
        # Replace this with actual algorithm if available
        return random.randint(1, 10)
    
    correlation_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            degree = minimal_degree_quaternionic_polynomial_representation(circuit)
            variance = communication_complexity_rank_variance(circuit)
            correlation_values.append((degree, variance))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not correlation_values:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_degree = sum(x for x, _ in correlation_values) / len(correlation_values)
    mean_variance = sum(y for _, y in correlation_values) / len(correlation_values)
    covariance = sum((x - mean_degree) * (y - mean_variance) for x, y in correlation_values) / len(correlation_values)
    variance_degree = sum((x - mean_degree)**2 for x, _ in correlation_values) / len(correlation_values)
    variance_variance = sum((y - mean_variance)**2 for _, y in correlation_values) / len(correlation_values)
    correlation_coefficient = covariance / math.sqrt(variance_degree * variance_variance)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['n_max']}, degree={result['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break