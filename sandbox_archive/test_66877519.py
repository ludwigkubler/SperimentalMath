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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def eta_invariant(graph):
        # Simplified version of the eta-invariant calculation for demonstration purposes
        n = len(graph)
        return Fraction(n * (n - 1) // 2, d)
    
    def monotone_width(graph):
        # Brute-force approach to calculate monotone width
        n = len(graph)
        max_width = 0
        for subset in range(1 << n):
            subset_nodes = [i for i in range(n) if (subset & (1 << i)) != 0]
            if all(len(graph[u].intersection(subset_nodes)) > 0 for u in subset_nodes):
                max_width = max(max_width, len(subset_nodes))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    width_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)
        if graph is None:
            continue
        eta = eta_invariant(graph)
        width = monotone_width(graph)
        eta_values.append(eta.numerator / eta.denominator)
        width_values.append(width)
    
    if len(eta_values) < 30 or len(width_values) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(eta_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    correlation = 0
    mean_eta = sum(eta_values) / len(eta_values)
    mean_width = sum(width_values) / len(width_values)
    for eta, width in zip(eta_values, width_values):
        correlation += (eta - mean_eta) * (width - mean_width)
    correlation /= math.sqrt(sum((eta - mean_eta)**2 for eta in eta_values)) * math.sqrt(sum((width - mean_width)**2 for width in width_values))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(eta_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7 and sum(abs(eta - mean_width * (mean_width / mean_eta)) for eta in eta_values) <= 2 * len(eta_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break