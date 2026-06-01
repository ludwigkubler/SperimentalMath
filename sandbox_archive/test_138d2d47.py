# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def is_planar(graph):
    if len(graph) <= 4:
        return True
    for u, v in combinations(graph.keys(), 2):
        subgraph = {u: graph[u], v: graph[v]}
        for w in set(graph.keys()) - {u, v}:
            if (w in subgraph[u] and w in subgraph[v]) or (v in subgraph[u] and u in subgraph[v]):
                return False
    return True

def generate_planar_graph(n):
    while True:
        nodes = list(range(1, n+1))
        edges = set()
        for _ in range(n-1):
            u, v = random.sample(nodes, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
                nodes.remove(u)
        graph = {node: [] for node in range(1, n+1)}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        if is_planar(graph):
            return graph

def term_overlap_graph(graph):
    n = len(graph)
    T = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            T[i].append(j) if any(v in graph[u] for u in range(n) if u != i and u != j) else None
            T[j].append(i) if any(u in graph[v] for v in range(n) if v != i and v != j) else None
    return [list(filter(None, t)) for t in T]

def minimal_rank(T):
    n = len(T)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if j in T[i]:
                A[i][j] = 1
                A[j][i] = 1
    rank = 0
    for row in A:
        if any(row):
            rank += 1
            for i in range(n):
                if row[i] and A[i][j]:
                    A[i][j] = 0
    return rank

def communication_complexity_growth_rate(graph, T):
    n = len(graph)
    growth_rate = 0
    for _ in range(10):  # Simulate multiple instances
        nodes = list(range(n))
        random.shuffle(nodes)
        subgraph = {node: graph[node] for node in nodes[:n//2]}
        T_sub = term_overlap_graph(subgraph)
        rank = minimal_rank(T_sub)
        growth_rate += rank
    return growth_rate / 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_planar_graph(n)
        T = term_overlap_graph(graph)
        rank = minimal_rank(T)
        growth_rate = communication_complexity_growth_rate(graph, T)
        results.append((rank, growth_rate))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ranks = [r for r, _ in results]
    growth_rates = [g for _, g in results]
    mean_rank = sum(ranks) / len(ranks)
    mean_growth_rate = sum(growth_rates) / len(growth_rates)
    covariance = sum((r - mean_rank) * (g - mean_growth_rate) for r, g in results)
    variance_rank = sum((r - mean_rank)**2 for r in ranks)
    variance_growth_rate = sum((g - mean_growth_rate)**2 for g in growth_rates)
    std_dev_rank = math.sqrt(variance_rank / len(ranks))
    std_dev_growth_rate = math.sqrt(variance_growth_rate / len(growth_rates))
    
    if std_dev_rank == 0 or std_dev_growth_rate == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "metric_saturation"
        }
    
    correlation_coefficient = covariance / (std_dev_rank * std_dev_growth_rate)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")