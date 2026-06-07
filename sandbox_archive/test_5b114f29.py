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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def compute_mld(graph):
        n = len(graph)
        if n == 0:
            return 0
        mld = float('inf')
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if j not in neighbors and any(k in graph[j] for k in neighbors):
                    mld = min(mld, len(neighbors))
        return mld
    
    def compute_entanglement_complexity(graph):
        n = len(graph)
        if n == 0:
            return 0
        entanglement = 0
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i]:
                    entanglement += 1
        return entanglement
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst):
        avg = mean(lst)
        return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    mld_values = []
    entanglement_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        mld = compute_mld(graph)
        entanglement = compute_entanglement_complexity(graph)
        mld_values.append(mld)
        entanglement_values.append(entanglement)
    
    if not mld_values or not entanglement_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (mean([mld * entanglement for mld, entanglement in zip(mld_values, entanglement_values)])
                   / (std(mld_values) * std(entanglement_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and std(mld_values) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_corr = std([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std={std_corr:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")