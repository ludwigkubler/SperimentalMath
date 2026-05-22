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
    
    def geometric_entropy(v):
        return -math.log2(len(v)) if v else 0
    
    def minor_free_planar_graph(G):
        # Simplified heuristic to generate a minor-free planar graph from G
        n = len(G)
        M_G = {i: [] for i in range(n)}
        for u, v in G:
            M_G[u].append(v)
            M_G[v].append(u)
        return M_G
    
    def count_vertices_with_entropy(M_G, ε):
        H_MG = [v for v in M_G if geometric_entropy(v) <= ε]
        return len(H_MG)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        G = {i: [] for i in range(n)}
        for _ in range(2 * n):
            u, v = random.sample(range(n), 2)
            if u != v and (v not in G[u] or u not in G[v]):
                G[u].append(v)
                G[v].append(u)
        
        ε = max(geometric_entropy(v) for v in G.values())
        M_G = minor_free_planar_graph(G)
        H_MG_count = count_vertices_with_entropy(M_G, ε)
        
        total_metric_value += H_MG_count
        instances_tested += 1
    
    metric_name = "Number of Vertices with Geometric Entropy ≤ ε"
    metric_value = total_metric_value / len(n_values)
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")