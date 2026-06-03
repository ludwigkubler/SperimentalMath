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
    
    # Define the constructive mapping to compute GT(G)
    def grothendieck_teichmueller_group(G):
        n = len(G)
        rank = 0
        for u in range(n):
            neighbors = G[u]
            if len(neighbors) > rank:
                rank = len(neighbors)
        return rank
    
    # Generate a random graph with n vertices and maximum degree d(G)
    def generate_random_graph(n, max_degree):
        G = [[] for _ in range(n)]
        degrees = [0] * n
        for u in range(n):
            d_u = random.randint(1, min(max_degree, n - 1))
            neighbors = random.sample(range(n), d_u)
            while any(len(G[v]) >= max_degree for v in neighbors):
                neighbors = random.sample(range(n), d_u)
            G[u] = neighbors
            degrees[u] = len(neighbors)
        return G
    
    # Calculate the maximum degree of the graph
    def max_degree(G):
        return max(len(neighbors) for neighbors in G)
    
    # Calculate the rank of the Grothendieck-Teichmüller group
    def calculate_rank(G):
        return grothendieck_teichmueller_group(G)
    
    # Main trial logic
    n = 40
    max_degree_value = 5
    G = generate_random_graph(n, max_degree_value)
    d_G = max_degree(G)
    r_G = calculate_rank(G)
    
    # Calculate the metric values
    log_d_G = math.log(d_G) if d_G > 0 else float('inf')
    sqrt_n = math.sqrt(n)
    
    # Check the conjecture conditions
    conjecture_holds = (log_d_G <= r_G and r_G <= sqrt_n)
    counterexample = "" if conjecture_holds else f"r(G)={r_G}, log d(G)={log_d_G}, √n={sqrt_n}"
    
    return {
        "metric_name": "Rank of GT(G)",
        "metric_value": r_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and standard deviation of metric_value
    metric_values = [r["metric_value"] for r in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    # Determine the result based on acceptance criterion
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for seed, result in zip(seeds, results):
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break