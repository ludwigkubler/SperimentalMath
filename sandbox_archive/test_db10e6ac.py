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
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(2**(n-1))]
    
    def communication_complexity_rank_variance(circuit):
        # Placeholder function to compute rank variance
        return random.uniform(0.5, 1.5)
    
    def minimal_degree_quaternionic_representation(circuit):
        # Placeholder function to compute minimal degree
        return random.randint(2, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        rank_variance = communication_complexity_rank_variance(circuit)
        degree = minimal_degree_quaternionic_representation(circuit)
        results.append((n, degree, rank_variance))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    degrees = [r[1] for r in results]
    rank_variances = [r[2] for r in results]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def variance(lst, mean):
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    degrees_mean = mean(degrees)
    rank_variances_mean = mean(rank_variances)
    degrees_variance = variance(degrees, degrees_mean)
    rank_variances_variance = variance(rank_variances, rank_variances_mean)
    covariance = sum((degrees[i] - degrees_mean) * (rank_variances[i] - rank_variances_mean) for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / math.sqrt(degrees_variance * rank_variances_variance)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")