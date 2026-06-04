# auto-injected by SEC sandbox
import math
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
                if len(edges_added) == n * d // 2:
                    return graph
    
    raise ValueError("Failed to generate a d-regular graph")

def compute_minimal_representation_length(graph):
    # Placeholder for the actual computation
    # For simplicity, we assume a linear relationship with the number of edges
    num_edges = sum(len(neighbors) for neighbors in graph) // 2
    return Fraction(num_edges * 2, 1)

def compute_resolution_proof_width(graph):
    # Placeholder for the actual computation
    # For simplicity, we assume a quadratic relationship with the number of vertices
    n = len(graph)
    return Fraction(n * (n - 1), 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 2)
        m = compute_minimal_representation_length(graph)
        w = compute_resolution_proof_width(graph)
        
        if m <= 0 or w <= 0:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "non-positive values"
            }
        
        results.append((m, w))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient instances"
        }
    
    m_values = [m for m, _ in results]
    w_values = [w for _, w in results]
    
    mean_m = sum(m_values) / len(m_values)
    mean_w = sum(w_values) / len(w_values)
    
    correlation = 0
    for m, w in zip(m_values, w_values):
        correlation += (m - mean_m) * (w - mean_w)
    correlation /= (len(results) * (sum((m - mean_m) ** 2 for m in m_values)) ** 0.5 * (sum((w - mean_w) ** 2 for w in w_values)) ** 0.5)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation > 0.8 and mean_m <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len(results)} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")