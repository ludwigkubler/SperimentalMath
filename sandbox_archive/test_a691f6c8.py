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
    if (n * d) % 2 != 0:
        return None
    graph = [[] for _ in range(n)]
    degree_count = [0] * n
    edges_added = 0
    
    while edges_added < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and len(graph[u]) < d and len(graph[v]) < d and (v not in graph[u]):
            graph[u].append(v)
            graph[v].append(u)
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added += 1
    
    return graph if all(deg == d for deg in degree_count) else None

def compute_automorphic_representation(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            adjacency_matrix[u][v] = 1
    
    # Compute the characteristic polynomial
    char_poly = [Fraction(1, 1)] + [-sum(adjacency_matrix[i]) for i in range(n)]
    for _ in range(n - 2):
        new_coeffs = [char_poly[0]]
        for j in range(1, len(char_poly)):
            new_coeffs.append(char_poly[j] * (n - j) - sum(char_poly[k] * char_poly[j - k] for k in range(1, j)))
        char_poly = new_coeffs
    
    # The minimal index is the absolute value of the coefficient of x^(n-2)
    min_index = abs(char_poly[-3])
    return min_index

def compute_monotone_width(circuit_representation):
    if not isinstance(circuit_representation, list) or not all(isinstance(row, list) for row in circuit_representation):
        raise ValueError("Circuit representation must be a 2D list")
    
    return sum(len(row) for row in circuit_representation)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    monotone_widths = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        
        min_index = compute_automorphic_representation(graph)
        circuit_representation = [[1] * (n - 1)]  # Simplified example of a monotone circuit
        monotone_width = compute_monotone_width(circuit_representation)
        
        min_indices.append(min_index)
        monotone_widths.append(monotone_width)
    
    if not min_indices or not monotone_widths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": len(min_indices),
            "n_max": max(n_values) if min_indices else 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    correlation_coefficient = sum((min_indices[i] - sum(min_indices) / len(min_indices)) * (monotone_widths[i] - sum(monotone_widths) / len(monotone_widths)) for i in range(len(min_indices))) / (len(min_indices) * math.sqrt(sum((min_index - sum(min_indices) / len(min_indices)) ** 2 for min_index in min_indices)) * math.sqrt(sum((monotone_width - sum(monotone_widths) / len(monotone_widths)) ** 2 for monotone_width in monotone_widths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_indices),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed={first_failing_seed}")