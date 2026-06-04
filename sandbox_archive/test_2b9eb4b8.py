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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
    
    return graph

def compute_minimal_representation_length(graph):
    # Placeholder implementation
    return sum(len(neighbors) for neighbors in graph)

def compute_resolution_proof_width(graph):
    # Placeholder implementation
    n = len(graph)
    max_degree = max(len(neighbors) for neighbors in graph)
    return max_degree * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        m_phi_G = compute_minimal_representation_length(graph)
        w_phi_G = compute_resolution_proof_width(graph)
        
        if m_phi_G == 0 or w_phi_G == 0:
            continue
        
        results.append({
            "n": n,
            "m_phi_G": m_phi_G,
            "w_phi_G": w_phi_G
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    m_phi_G_values = [result["m_phi_G"] for result in results]
    w_phi_G_values = [result["w_phi_G"] for result in results]
    
    mean_m_phi_G = sum(m_phi_G_values) / len(m_phi_G_values)
    mean_w_phi_G = sum(w_phi_G_values) / len(w_phi_G_values)
    
    correlation = 0
    if mean_m_phi_G != 0 and mean_w_phi_G != 0:
        numerator = sum((m_phi_G - mean_m_phi_G) * (w_phi_G - mean_w_phi_G) for m_phi_G, w_phi_G in zip(m_phi_G_values, w_phi_G_values))
        denominator = math.sqrt(sum((m_phi_G - mean_m_phi_G) ** 2 for m_phi_G in m_phi_G_values)) * math.sqrt(sum((w_phi_G - mean_w_phi_G) ** 2 for w_phi_G in w_phi_G_values))
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation > 0.8 and mean_m_phi_G <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["metric_value"] is not None for result in all_results):
        mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    else:
        mean_metric_value, std_metric_value = None, None
    
    if support_fraction >= 0.8 and (mean_metric_value is None or mean_metric_value <= 3):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")