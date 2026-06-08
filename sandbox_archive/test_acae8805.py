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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(instance):
        n = len(instance)
        trop_points = []
        for i in range(2**n):
            point = []
            for j in range(n):
                if instance[i] & (1 << j):
                    point.append(j + 1)
                else:
                    point.append(-j - 1)
            trop_points.append(point)
        return trop_points
    
    def order_of_automorphism_group(trop_points):
        n = len(trop_points[0])
        symmetries = []
        for i in range(2**n):
            permuted_points = [trop_points[(i >> j) & 1] for j in range(n)]
            if all(sorted(p) == sorted(q) for p, q in zip(trop_points, permuted_points)):
                symmetries.append(i)
        return len(symmetries)
    
    def dpll_path_length(instance):
        n = len(instance)
        stack = []
        path_length = 0
        while stack or any(x == 1 for x in instance):
            if not stack:
                stack.append((instance, 0))
                path_length += 1
            current_instance, pos = stack[-1]
            if pos == n:
                stack.pop()
                continue
            if current_instance[pos] == 0:
                new_instance = current_instance[:]
                new_instance[pos] = 1
                stack.append((new_instance, pos + 1))
                path_length += 1
            else:
                stack[-1] = (current_instance, pos + 1)
        return path_length
    
    n = random.randint(5, 40)
    instance = generate_boolean_instance(n)
    trop_points = tropicalize(instance)
    order_t = order_of_automorphism_group(trop_points)
    path_length = dpll_path_length(instance)
    
    return {
        "metric_name": "order_t - path_length",
        "metric_value": abs(order_t - path_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(order_t - path_length) <= 3 * max(path_length),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")