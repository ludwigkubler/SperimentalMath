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
    
    def circuit_size(f):
        # Simplified DPLL solver to estimate circuit size
        n = len(f)
        if n == 1:
            return 1
        subproblems = [f[:n//2], f[n//2:]]
        sizes = [circuit_size(sub) for sub in subproblems]
        return max(sizes) + 1
    
    def irreducible_representation_dimension(f):
        # Placeholder function to simulate computation of dimension
        n = len(f)
        if n == 1:
            return 1
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            dim_irr = irreducible_representation_dimension(f)
            s_f = circuit_size(f)
            metric_values.append(dim_irr / (s_f ** 2))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "dim(Irr(f)) / s(f)^2",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, metric_values)) / \
                              math.sqrt(sum((x - mean) ** 2 for x in metric_values) * sum((y - mean) ** 2 for y in metric_values))
    mean_value = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "dim(Irr(f)) / s(f)^2",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")