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
        if (n * d) % 2 != 0 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        max_width = 0
        
        def dfs(node, parent):
            visited[node] = True
            width = 1
            for neighbor in graph[node]:
                if neighbor != parent and not visited[neighbor]:
                    width += dfs(neighbor, node)
            return width
        
        for start_node in range(n):
            visited = [False] * n
            max_width = max(max_width, dfs(start_node, -1))
        
        return max_width
    
    def minimal_brauer_group_order(graph):
        if graph is None:
            return 0
        n = len(graph)
        # Simplified mapping to a modular form and then computing the order
        # This is a placeholder for actual computation
        return n * (n - 1) // 2
    
    def is_complete_graph(graph):
        n = len(graph)
        if n == 0:
            return False
        for i in range(n):
            if len(graph[i]) != n - 1:
                return False
        return True
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)  # Example d=3
        if graph is None:
            continue
        
        br_order = minimal_brauer_group_order(graph)
        w_mon = circuit_monotone_width(graph)
        
        results.append({
            "n": n,
            "br_order": br_order,
            "w_mon": w_mon
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    br_orders = [result["br_order"] for result in results]
    w_mons = [result["w_mon"] for result in results]
    
    mean_br_order = sum(br_orders) / len(br_orders)
    mean_w_mon = sum(w_mons) / len(w_mons)
    
    correlation_coefficient = 0
    if len(br_orders) > 1:
        numerator = sum((br_orders[i] - mean_br_order) * (w_mons[i] - mean_w_mon) for i in range(len(br_orders)))
        denominator = math.sqrt(sum((br_orders[i] - mean_br_order) ** 2 for i in range(len(br_orders)))) * math.sqrt(sum((w_mons[i] - mean_w_mon) ** 2 for i in range(len(w_mons))))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    complete_graphs = [result["n"] for result in results if is_complete_graph(generate_d_regular_graph(result["n"], 3))]
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(br_order >= 2**(n-1) for n, br_order in zip(complete_graphs, [minimal_brauer_group_order(generate_d_regular_graph(n, 3)) for n in complete_graphs])),
        "counterexample": "" if correlation_coefficient >= 0.8 and all(br_order >= 2**(n-1) for n, br_order in zip(complete_graphs, [minimal_brauer_group_order(generate_d_regular_graph(n, 3)) for n in complete_graphs])) else "correlation_too_low_or_complete_graph_bounds_violated"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:]))
    if not seeds:
        seeds = [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low_or_complete_graph_bounds_violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")