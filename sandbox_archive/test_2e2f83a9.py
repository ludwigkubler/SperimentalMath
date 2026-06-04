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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        visited = [False] * n
        stack = []
        
        def dfs(node):
            nonlocal visited, stack
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
            stack.append(node)
        
        for node in range(n):
            if not visited[node]:
                dfs(node)
        
        transpose_graph = {i: [] for i in range(n)}
        for u, v in graph.items():
            for neighbor in v:
                transpose_graph[neighbor].append(u)
        
        def dfs_transpose(node):
            nonlocal visited
            visited[node] = True
            for neighbor in transpose_graph[node]:
                if not visited[neighbor]:
                    dfs_transpose(neighbor)
        
        count = 0
        while stack:
            node = stack.pop()
            if not visited[node]:
                count += 1
                dfs_transpose(node)
        
        return count
    
    def integer_lattice_homology(graph):
        n = len(graph)
        if n == 0:
            return 0
        rank = 0
        for i in range(n):
            row = [1] * n
            for neighbor in graph[i]:
                row[neighbor] += 1
            if all(x % 2 == 0 for x in row):
                rank += 1
        return rank
    
    def correlation_coefficient(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        numerator = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n))
        denominator = math.sqrt(sum((values1[i] - mean1) ** 2 for i in range(n))) * math.sqrt(sum((values2[i] - mean2) ** 2 for i in range(n)))
        if denominator == 0:
            return 0
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        homology_rank = integer_lattice_homology(graph)
        width = circuit_monotone_width(graph)
        results.append((homology_rank, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    homology_ranks = [x[0] for x in results]
    widths = [x[1] for x in results]
    corr_coeff = correlation_coefficient(homology_ranks, widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.5 and corr_coeff < 0.7,
        "counterexample": "" if corr_coeff > 0.5 and corr_coeff < 0.7 else f"correlation_coefficient={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(x["conjecture_holds"] for x in results):
        mean_value = sum(x["metric_value"] for x in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")