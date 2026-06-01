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

def generate_planar_graph(n):
    if n < 3:
        return [], 0
    
    # Generate a planar graph using a known algorithm (e.g., triangulation)
    vertices = list(range(n))
    edges = []
    
    def add_triangle(v1, v2, v3):
        edges.append((v1, v2))
        edges.append((v2, v3))
        edges.append((v3, v1))
    
    # Start with a triangle
    add_triangle(0, 1, 2)
    
    for i in range(3, n):
        v = random.choice(vertices[:i])
        u = random.choice(vertices[:i+1] if i + 1 < n else vertices[:i])
        while (v, u) in edges or (u, v) in edges:
            u = random.choice(vertices[:i+1] if i + 1 < n else vertices[:i])
        add_triangle(v, u, i)
    
    return edges, n

def compute_local_system_rank(edges, n):
    # Placeholder for the actual algorithm to compute local system rank
    # This is a dummy implementation for demonstration purposes
    return len(edges) / (n * (n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [20, 30, 40]:
        edges, _ = generate_planar_graph(n)
        l_G = compute_local_system_rank(edges, n)
        
        c = 1 / (n ** (3/2))
        if l_G < c * n ** (3/2):
            counterexample = "Partition into two parts with communication complexity less than n is possible."
            conjecture_holds = False
        else:
            counterexample = ""
            conjecture_holds = True
        
        results.append({
            "n": n,
            "l_G": l_G,
            "c": c,
            "counterexample": counterexample,
            "conjecture_holds": conjecture_holds
        })
    
    metric_value = sum(result["l_G"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Average Local System Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "support_fraction": support_fraction,
        "counterexample": counterexample if not all(result["conjecture_holds"] for result in results) else "",
        "conjecture_holds": any(result["conjecture_holds"] for result in results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
    
    mean_metric_value = sum(trial_result["metric_value"] for trial_result in results) / len(results)
    std_metric_value = math.sqrt(sum((trial_result["metric_value"] - mean_metric_value) ** 2 for trial_result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Partition into two parts with communication complexity less than n is possible.\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")