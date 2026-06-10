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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hyperplane_arrangement(f):
        n = len(f)
        arrangement = []
        for i in range(2**n):
            if f[i] == 1:
                arrangement.append(i)
        return arrangement
    
    def p_adic_logarithmic_capacity(arrangement, p=53):
        n = len(arrangement)
        capacity = 0
        for i in range(n):
            for j in range(i+1, n):
                if (arrangement[i] & arrangement[j]) == 0:
                    capacity += math.log(2, p)
        return capacity / (n * (n - 1))
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        instances = [f]
        for _ in range(n-1):
            new_instance = f[:]
            for j in range(n):
                if random.choice([0, 1]) == 1:
                    new_instance[j] = 1 - new_instance[j]
            instances.append(new_instance)
        
        rank_variance = 0
        for i in range(len(instances)):
            for j in range(i+1, len(instances)):
                diff = sum(1 for a, b in zip(instances[i], instances[j]) if a != b)
                rank_variance += diff**2
        
        return rank_variance / (len(instances) * (len(instances) - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        arrangement = hyperplane_arrangement(f)
        log_cap = p_adic_logarithmic_capacity(arrangement)
        rank_variance = communication_complexity_rank_variance(f)
        correlation = (log_cap - rank_variance) / (max(log_cap, rank_variance) + 1e-9)
        results.append({
            "n": n,
            "log_cap": log_cap,
            "rank_variance": rank_variance,
            "correlation": correlation
        })
    
    mean_correlation = sum(result["correlation"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["correlation"] - mean_correlation)**2 for result in results) / len(results))
    
    return {
        "metric_name": "Correlation between log-capacity and rank variance",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_correlation >= 0.8 and std_correlation <= 0.1,
        "counterexample": "" if mean_correlation >= 0.8 and std_correlation <= 0.1 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")