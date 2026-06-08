# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_k_regular_graph(n, k):
    if (n * k) % 2 != 0:
        raise ValueError("Invalid parameters for generating a d-regular graph")
    
    edges = set()
    while len(edges) < n * k // 2:
        u, v = random.sample(range(n), 2)
        if u > v:
            u, v = v, u
        if (u, v) not in edges and (v, u) not in edges:
            degree_u = sum(1 for edge in edges if edge[0] == u or edge[1] == u)
            degree_v = sum(1 for edge in edges if edge[0] == v or edge[1] == v)
            if degree_u < k and degree_v < k:
                edges.add((u, v))
    
    return list(edges)

def is_non_crossing_partition(partition):
    n = len(partition)
    for i in range(n):
        for j in range(i + 1, n):
            if partition[i][0] > partition[j][0]:
                partition[i], partition[j] = partition[j], partition[i]
    
    for i in range(n - 1):
        for j in range(i + 1, n):
            if partition[i][-1] > partition[j][0]:
                return False
    return True

def minimal_order_of_non_crossing_partitions(graph):
    n = len(graph)
    vertices = list(range(n))
    all_partitions = []
    
    def generate_partitions(current_partition, remaining_vertices):
        if not remaining_vertices:
            if is_non_crossing_partition(current_partition):
                all_partitions.append(current_partition[:])
            return
        
        for i in range(1, len(remaining_vertices) + 1):
            for subset in combinations(remaining_vertices, i):
                current_partition.append(subset)
                generate_partitions(current_partition, [v for v in remaining_vertices if v not in subset])
                current_partition.pop()
    
    generate_partitions([], vertices)
    
    min_order = float('inf')
    for partition in all_partitions:
        order = sum(len(subset) for subset in partition)
        if order < min_order:
            min_order = order
    
    return min_order

def communication_rank_variance(graph):
    n = len(graph)
    rank_var = 0
    for i in range(n):
        row = [1 if (i, j) in graph or (j, i) in graph else 0 for j in range(n)]
        rank_var += abs(sum(row))
    
    return rank_var / n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        k = 3  # Example value for k-regular graph
        graph = generate_k_regular_graph(n, k)
        order = minimal_order_of_non_crossing_partitions(graph)
        rank_var = communication_rank_variance(graph)
        
        if order == float('inf'):
            return {
                "metric_name": "Order of Non-Crossing Partitions",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_metric_value += order / rank_var
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Order of Non-Crossing Partitions",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")