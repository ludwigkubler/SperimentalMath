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

def generate_random_graph(n):
    if n <= 1:
        return []
    
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    
    return list(edges)

def communication_complexity_rank(G):
    # Placeholder function to simulate the computation of communication complexity rank
    return len(G) ** 2

def minimal_order_of_quaternionic_kähler_forms(M):
    # Placeholder function to simulate the computation of minimal order of quaternionic Kähler forms
    return len(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        M = G
        o_G = minimal_order_of_quaternionic_kähler_forms(M)
        r_G = communication_complexity_rank(G)
        
        if o_G == 0 or r_G == 0:
            continue
        
        results.append({
            "n": n,
            "o_G": o_G,
            "r_G": r_G
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    o_G_values = [r["o_G"] for r in results]
    r_G_values = [r["r_G"] for r in results]
    
    mean_o_G = sum(o_G_values) / len(o_G_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    
    covariance = sum((o_G - mean_o_G) * (r_G - mean_r_G) for o_G, r_G in zip(o_G_values, r_G_values)) / len(o_G_values)
    variance_o_G = sum((o_G - mean_o_G) ** 2 for o_G in o_G_values) / len(o_G_values)
    variance_r_G = sum((r_G - mean_r_G) ** 2 for r_G in r_G_values) / len(r_G_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_o_G) * math.sqrt(variance_r_G))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "insufficient_instances"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")