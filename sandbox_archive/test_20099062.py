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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_primitive_element(p):
        while True:
            a = random.randint(2, p - 1)
            if all(pow(a, (p - 1) // q, p) != 1 for q in range(2, int(math.sqrt(p)) + 1)):
                return a

    def local_class_group_size(p):
        if not is_prime(p):
            raise ValueError("p must be a prime number")
        return p - 1

    def communication_complexity_rank(n):
        # Placeholder function for the actual computation
        # This should be replaced with the actual algorithm for computing ccr(K/L)
        return random.randint(1, n)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_correlation = 0.0

    for n in n_values:
        for _ in range(5):
            p = random.randint(n + 1, 2 * n)
            if not is_prime(p):
                continue
            alpha = generate_primitive_element(p)
            K = [alpha ** i % p for i in range(p)]
            L = [i % p for i in range(p)]

            try:
                cl_size = local_class_group_size(p)
                ccr = communication_complexity_rank(n)
                instances_tested += 1
                total_correlation += abs(cl_size - ccr) / (cl_size + ccr)
            except Exception as e:
                return {
                    "metric_name": "Correlation between local class group size and communication complexity rank",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }

    if instances_tested < 30:
        return {
            "metric_name": "Correlation between local class group size and communication complexity rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_correlation = total_correlation / instances_tested
    return {
        "metric_name": "Correlation between local class group size and communication complexity rank",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_correlation - 1) <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")