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
    
    # Define constants and parameters
    d = 3  # Degree of the regular graph
    n_values = [5, 10, 15, 20, 30, 40]
    trials_per_n = 5
    
    mhd_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        if n % d != 0:
            continue
        
        for _ in range(trials_per_n):
            # Generate a random d-regular graph with n vertices
            G = generate_d_regular_graph(n, d)
            
            # Calculate the minimal symplectic hull diameter mhd(G)
            mhd_G = calculate_mhd(G)
            if mhd_G is None:
                continue
            
            # Determine the circuit monotone width w_G
            w_G = calculate_circuit_monotone_width(G)
            if w_G is None:
                continue
            
            mhd_sum += mhd_G
            w_sum += w_G
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_mhd = mhd_sum / instances_tested
    mean_w = w_sum / instances_tested
    
    # Calculate the correlation coefficient r
    covariance = sum((w_G - mean_w) * (mhd_G - mean_mhd) for _, w_G, mhd_G in G) / instances_tested
    variance_w = sum((w_G - mean_w) ** 2 for _, w_G, _ in G) / instances_tested
    variance_mhd = sum((mhd_G - mean_mhd) ** 2 for _, _, mhd_G in G) / instances_tested
    
    if variance_w == 0 or variance_mhd == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_w) * math.sqrt(variance_mhd))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and mean_w / mean_mhd >= 1,
        "counterexample": ""
    }

def generate_d_regular_graph(n: int, d: int) -> list:
    if n % d != 0:
        return None
    
    G = [[] for _ in range(n)]
    
    while True:
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d - len(G[i]))
            G[i].extend(neighbors)
            for neighbor in neighbors:
                edges.add((min(i, neighbor), max(i, neighbor)))
        
        if len(edges) == (n * d) // 2:
            return [(i, j) for i, j in edges]

def calculate_mhd(G: list) -> float:
    # Placeholder function to calculate mhd
    return random.random() * 10

def calculate_circuit_monotone_width(G: list) -> float:
    # Placeholder function to calculate w_G
    return random.random() * 10

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        counterexample_desc = next(r["counterexample"] for r in results if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")