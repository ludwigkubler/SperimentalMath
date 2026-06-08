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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0 or k < 1 or k >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < k and len(graph[j]) < k:
                    edges.add((i, j))
        while len(edges) > (n * k) // 2:
            u, v = random.choice(list(edges))
            graph[u].append(v)
            graph[v].append(u)
            edges.remove((u, v))
        return graph
    
    def is_non_crossing_partition(partition):
        n = len(partition)
        for i in range(n):
            for j in range(i + 1, n):
                if partition[i] & partition[j]:
                    return False
        return True
    
    def min_order_non_crossing_partitions(graph):
        n = len(graph)
        nodes = list(range(n))
        partitions = []
        for mask in range(1 << n):
            part = [set() for _ in range(n)]
            for i in range(n):
                if (mask >> i) & 1:
                    part[i].add(i)
            if is_non_crossing_partition(part):
                partitions.append(part)
        min_order = float('inf')
        for partition in partitions:
            order = sum(len(subset) for subset in partition)
            if order < min_order:
                min_order = order
        return min_order
    
    def communication_rank_variance(graph):
        n = len(graph)
        rank_var = 0
        for i in range(n):
            row = [1 if j in graph[i] else 0 for j in range(n)]
            rank_var += sum(row[j] * row[k] for j in range(k + 1, n)) / (n - k - 1)
        return rank_var
    
    def generate_random_k_regular_graphs(n, k, num_graphs):
        graphs = []
        while len(graphs) < num_graphs:
            graph = generate_k_regular_graph(n, k)
            if graph is not None and graph not in graphs:
                graphs.append(graph)
        return graphs
    
    n_values = [5, 10, 15, 20, 30, 40]
    all_orders = []
    all_rank_vars = []
    
    for n in n_values:
        graphs = generate_random_k_regular_graphs(n, n - 1, 30)
        if not graphs:
            return {
                "metric_name": "min_order_non_crossing_partitions",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        for graph in graphs:
            order = min_order_non_crossing_partitions(graph)
            rank_var = communication_rank_variance(graph)
            all_orders.append(order)
            all_rank_vars.append(rank_var)
    
    if not all_orders or not all_rank_vars:
        return {
            "metric_name": "min_order_non_crossing_partitions",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((all_orders[i] - mean_order) * (all_rank_vars[i] - mean_rank_var)
                                 for i in range(len(all_orders))) / len(all_orders)
    mean_order = sum(all_orders) / len(all_orders)
    mean_rank_var = sum(all_rank_vars) / len(all_rank_vars)
    
    if correlation_coefficient < 0.7 or any(order / rank_var > 1.5 for order, rank_var in zip(all_orders, all_rank_vars)):
        return {
            "metric_name": "min_order_non_crossing_partitions",
            "metric_value": None,
            "instances_tested": len(all_orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "min_order_non_crossing_partitions",
        "metric_value": correlation_coefficient,
        "instances_tested": len(all_orders),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")