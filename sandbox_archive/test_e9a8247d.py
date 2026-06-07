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
    
    def generate_random_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_cyclotomic_polynomial(instance):
        degree = len(instance)
        if degree == 1:
            return 1
        poly = [1]
        for i in range(1, degree):
            new_poly = [0] * (degree + i - 1)
            for j in range(degree):
                new_poly[j + i - 1] += poly[j] * instance[j]
            poly = new_poly
        return max(poly)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 30
        total_degree = 0
        
        for _ in range(instances_tested):
            instance = generate_random_boolean_instance(n)
            degree = tropical_cyclotomic_polynomial(instance)
            total_degree += degree
        
        mean_degree = total_degree / instances_tested
        conjecture_holds = mean_degree >= n ** (1/3)
        
        results.append({
            "n": n,
            "mean_degree": mean_degree,
            "conjecture_holds": conjecture_holds
        })
    
    metric_value = sum(result["mean_degree"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Mean Degree",
        "metric_value": metric_value,
        "instances_tested": instances_tested * len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else "support_fraction < 0.95"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.95' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.95")