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
                if len(edges_added) == (n * d) // 2:
                    return graph
    
    raise ValueError("Failed to generate a d-regular graph")

def topological_entropy(graph):
    n = len(graph)
    degree_sum = sum(len(neighbors) for neighbors in graph)
    avg_degree = Fraction(degree_sum, n)
    
    # Approximate the topological entropy using the average degree
    return avg_degree

def resolution_proof_width(n):
    # A simple heuristic: width is proportional to the number of variables
    return n // 2

def pearson_correlation_coefficient(data1, data2):
    n = len(data1)
    if n != len(data2):
        raise ValueError("Data sets must have the same length")
    
    mean_x = sum(data1) / n
    mean_y = sum(data2) / n
    
    numerator = sum((data1[i] - mean_x) * (data2[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((data1[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((data2[i] - mean_y) ** 2 for i in range(n)))
    
    return numerator / denominator if denominator != 0 else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    graph = generate_d_regular_graph(n, d)
    
    h_G = topological_entropy(graph)
    w_phi_G = resolution_proof_width(n)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient([h_G], [w_phi_G]),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if pearson_correlation_coefficient([h_G], [w_phi_G]) < 0.5 else True,
        "counterexample": "" if pearson_correlation_coefficient([h_G], [w_phi_G]) >= 0.7 else f"Correlation coefficient {pearson_correlation_coefficient([h_G], [w_phi_G])} is below the threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient below threshold' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")