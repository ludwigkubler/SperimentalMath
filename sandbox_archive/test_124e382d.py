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

def generate_random_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    
    graph = {i: [] for i in range(n)}
    edges = set()
    
    def add_edge(u, v):
        if u not in graph[v]:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((min(u, v), max(u, v)))
    
    while len(edges) < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and (u, v) not in edges and (v, u) not in edges:
            add_edge(u, v)
    
    return graph

def generate_circuit_and_rank(graph):
    # Placeholder for actual quantum ternary logic circuit generation
    # This is a dummy implementation that returns random values
    rank = random.randint(1, 10)
    width = random.randint(1, 20)
    return rank, width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlations = []
    
    for n in n_values:
        d = min(2 * (n - 1), n // 2)  # Ensure the graph is regular
        G = generate_random_d_regular_graph(n, d)
        
        if G is None:
            continue
        
        rank, width = generate_circuit_and_rank(G)
        correlations.append((rank, width))
    
    if len(correlations) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": len(correlations),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    ranks = [corr[0] for corr in correlations]
    widths = [corr[1] for corr in correlations]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    
    covariance = sum((r - mean_rank) * (w - mean_width) for r, w in correlations) / len(correlations)
    variance_rank = sum((r - mean_rank) ** 2 for r in ranks) / len(ranks)
    variance_width = sum((w - mean_width) ** 2 for w in widths) / len(widths)
    
    pearson_corr = covariance / (math.sqrt(variance_rank) * math.sqrt(variance_width))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(correlations),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7 and pearson_corr <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if not math.isnan(result["metric_value"])) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if not math.isnan(result["metric_value"])) / len(results))
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not math.isnan(result["metric_value"]) and result["metric_value"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not math.isnan(result["metric_value"]) and result["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"value_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")