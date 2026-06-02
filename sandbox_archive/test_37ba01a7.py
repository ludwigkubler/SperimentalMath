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
    n = 40
    d = 3
    instances_tested = 0
    total_br = 0
    total_w_mon = 0
    n_max = 0
    
    for _ in range(30):
        # Generate a random d-regular graph on n vertices
        G = generate_d_regular_graph(n, d)
        if not G:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        
        # Compute the minimal order of the brauer group (br(G))
        br_G = compute_brauer_group_order(G)
        total_br += br_G
        
        # Calculate the circuit monotone width w_mon(G)
        w_mon_G = calculate_circuit_monotone_width(G)
        total_w_mon += w_mon_G
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    # Compute the Pearson correlation coefficient
    mean_br = total_br / instances_tested
    mean_w_mon = total_w_mon / instances_tested
    numerator = sum((br_G - mean_br) * (w_mon_G - mean_w_mon) for br_G, w_mon_G in zip(br_values, w_mon_values))
    denominator = math.sqrt(sum((br_G - mean_br)**2 for br_G in br_values)) * math.sqrt(sum((w_mon_G - mean_w_mon)**2 for w_mon_G in w_mon_values))
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    # Check the lower bound on br(G) for complete graphs
    is_complete_graph = all(len(G[i]) == n-1 for i in range(n))
    conjecture_holds = correlation_coefficient >= 0.8 and (is_complete_graph or br_G >= 2**(n-1))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < n * d // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        if u == v or (u, v) in edges_added or (v, u) in edges_added:
            continue
        
        G[u].append(v)
        G[v].append(u)
        edges_added.add((u, v))
    
    return G

def compute_brauer_group_order(G):
    # Placeholder for the actual computation of the brauer group order
    # This is a dummy implementation and should be replaced with the actual algorithm
    return random.randint(1, 100)

def calculate_circuit_monotone_width(G):
    # Placeholder for the actual calculation of the circuit monotone width
    # This is a dummy implementation and should be replaced with the actual algorithm
    return random.randint(1, 100)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")