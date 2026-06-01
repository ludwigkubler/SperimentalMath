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
    
    def generate_instance(n):
        # Generate a random communication complexity instance with n bits
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_stabilizer_group(instance):
        # Compute the stabilizer group of the instance
        n = len(instance)
        T = set()
        for i in range(2**n):
            if all(instance[j] == (i >> j) & 1 for j in range(n)):
                T.add(i)
        return T
    
    def compute_min_generators(group):
        # Compute the minimum number of generators for the group
        n = len(group)
        if n == 0:
            return 0
        generators = []
        for i in range(1, n):
            if all((g >> j) & 1 != (i >> j) & 1 for g in generators):
                generators.append(i)
        return len(generators)
    
    def compute_communication_rank(instance):
        # Compute the communication rank of the instance
        n = len(instance)
        r = 0
        for i in range(n):
            if any(instance[j] == (i >> j) & 1 for j in range(i+1, n)):
                r += 1
        return r
    
    def correlation_coefficient(x, y):
        # Compute the correlation coefficient between two lists
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for _ in range(30):
        instance = generate_instance(random.randint(5, 40))
        T = compute_stabilizer_group(instance)
        generators = compute_min_generators(T)
        r = compute_communication_rank(instance)
        results.append((generators, r))
    
    n_max = max(len(instance) for instance in results)
    if n_max < 16:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    generators = [result[0] for result in results]
    ranks = [result[1] for result in results]
    correlation = correlation_coefficient(generators, ranks)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")