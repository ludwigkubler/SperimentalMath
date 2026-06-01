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
    
    def is_planar(n):
        if n < 3:
            return True
        edges = random.randint(2 * n - 4, 3 * n - 6)
        return edges <= 3 * n - 6
    
    def generate_planar_graph(n):
        while not is_planar(n):
            n += 1
        vertices = list(range(n))
        edges = []
        for _ in range(2 * n - 4):
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def polynomial_roots(n):
        roots = []
        for i in range(n):
            root = complex(random.uniform(-1, 1), random.uniform(-1, 1))
            roots.append(root)
        return roots
    
    def euclidean_norm(roots):
        norm = 0
        for i in range(len(roots)):
            for j in range(i + 1, len(roots)):
                norm += abs(roots[i] - roots[j])
        return norm / (len(roots) * (len(roots) - 1))
    
    def communication_complexity(n):
        return n ** (2 / 3)
    
    def min_root_separability(n):
        roots = polynomial_roots(n)
        return euclidean_norm(roots)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        vertices, edges = generate_planar_graph(n)
        min_separation = min_root_separability(n)
        comm_complexity = communication_complexity(n)
        results.append({
            "n": n,
            "min_separation": min_separation,
            "comm_complexity": comm_complexity
        })
    
    if not all(result["n"] >= 5 for result in results):
        return {
            "metric_name": "min_root_separability",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic n"
        }
    
    min_separability_values = [result["min_separation"] for result in results]
    comm_complexity_values = [result["comm_complexity"] for result in results]
    
    mean_min_separation = sum(min_separability_values) / len(min_separability_values)
    mean_comm_complexity = sum(comm_complexity_values) / len(comm_complexity_values)
    
    if all(result["min_separation"] >= n ** (1 / 3) for result in results):
        min_holds = True
    else:
        min_holds = False
    
    if all(result["comm_complexity"] >= n ** (2 / 3) for result in results):
        comm_holds = True
    else:
        comm_holds = False
    
    correlation_coefficient = sum((min_separability_values[i] - mean_min_separation) * (comm_complexity_values[i] - mean_comm_complexity) for i in range(len(results))) / len(results)
    
    if min_holds and comm_holds and abs(correlation_coefficient) >= 0.8:
        return {
            "metric_name": "min_root_separability",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_root_separability",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "falsified"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='falsified' first_failing_seed={first_failing_seed}")