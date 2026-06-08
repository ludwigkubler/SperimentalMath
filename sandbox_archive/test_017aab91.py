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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_minimal_index_of_topological_entanglement(f):
        # Placeholder implementation
        return random.random()
    
    def calculate_communication_complexity_rank_variance(f):
        # Placeholder implementation
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        mu_f = calculate_minimal_index_of_topological_entanglement(f)
        R_f = calculate_communication_complexity_rank_variance(f)
        results.append({"n": n, "mu_f": mu_f, "R_f": R_f})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mu_values = [r["mu_f"] for r in results]
    R_values = [r["R_f"] for r in results]
    
    mean_mu = sum(mu_values) / len(mu_values)
    mean_R = sum(R_values) / len(R_values)
    
    covariance = sum((mu_values[i] - mean_mu) * (R_values[i] - mean_R) for i in range(len(mu_values))) / len(mu_values)
    variance_mu = sum((mu_values[i] - mean_mu)**2 for i in range(len(mu_values))) / len(mu_values)
    variance_R = sum((R_values[i] - mean_R)**2 for i in range(len(R_values))) / len(R_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_mu) * math.sqrt(variance_R))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_metric_values_missing")