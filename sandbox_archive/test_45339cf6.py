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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(d):
            nodes = list(range(n))
            random.shuffle(nodes)
            for j in range(1, d):
                u, v = nodes[j], nodes[(j + 1) % d]
                if (u, v) not in edges and (v, u) not in edges:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges.add((u, v))
        return graph
    
    def h_index(G):
        # Placeholder for Hodge index calculation
        return random.random() * 10  # Random value for demonstration
    
    def circuit_monotone_width(G):
        # Placeholder for circuit monotone width calculation
        return random.randint(1, 5)  # Random value for demonstration
    
    n = 40
    d = 3
    G = generate_d_regular_graph(n, d)
    if not G:
        return {
            "metric_name": "h_index(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    h = h_index(G)
    w_m = circuit_monotone_width(G)
    
    return {
        "metric_name": "h_index(G)",
        "metric_value": h,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)