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

def generate_xor_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def euclidean_distance(x, y):
    return sum((xi - yi) ** 2 for xi, yi in zip(x, y)) ** 0.5

def construct_metric_space(f):
    n = len(f)
    metric_space = {}
    for i in range(2**n):
        x = [int(b) for b in f"{i:0{n}b}"]
        for j in range(i + 1, 2**n):
            y = [int(b) for b in f"{j:0{n}b}"]
            metric_space[(tuple(x), tuple(y))] = euclidean_distance(x, y)
    return metric_space

def riemannian_curvature_tensor(metric_space):
    n = len(next(iter(metric_space)))
    tensor = {}
    for (x1, x2), d1 in metric_space.items():
        for (y1, y2), d2 in metric_space.items():
            if x1 == y1 and x2 == y2:
                continue
            numerator = 0
            denominator = 0
            for z in range(2**n):
                z_x1 = [int(b) for b in f"{z:0{n}b}"]
                z_y1 = [int(b) for b in f"{z:0{n}b}"]
                d3 = euclidean_distance(z_x1, z_y1)
                numerator += (d1 * d2 - d3**2) / (d1 + d2 - 2 * d3)
                denominator += (d1 + d2 - 2 * d3)**2
            tensor[(x1, x2, y1, y2)] = numerator / denominator
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_xor_function(n)
        metric_space = construct_metric_space(f)
        curvature_tensor = riemannian_curvature_tensor(metric_space)
        
        lower_bound = math.sqrt(n)
        upper_bound = 2 * math.sqrt(n)
        
        for (x1, x2, y1, y2), value in curvature_tensor.items():
            if value < lower_bound or value > upper_bound:
                return {
                    "metric_name": "Riemannian Curvature Tensor",
                    "metric_value": value,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Curvature tensor {value} is not in the range [{lower_bound}, {upper_bound}]"
                }
    
    return {
        "metric_name": "Riemannian Curvature Tensor",
        "metric_value": None,  # Not applicable for this conjecture
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_message = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_message = f"FALSIFIED counterexample=\"Curvature tensor out of bounds\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result_message}")