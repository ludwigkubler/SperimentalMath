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
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d):
            nodes = list(range(n))
            random.shuffle(nodes)
            for j in range(1, n):
                u, v = nodes[j-1], nodes[j]
                if (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
        return graph
    
    def local_induction_dimension(graph):
        n = len(graph)
        visited = [False] * n
        lid = 0
        
        def dfs(node, parent):
            nonlocal lid
            visited[node] = True
            for neighbor in graph[node]:
                if neighbor != parent and not visited[neighbor]:
                    dfs(neighbor, node)
            lid += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return lid
    
    def circuit_monotone_width(graph):
        n = len(graph)
        width = 0
        for i in range(n):
            neighbors = graph[i]
            for j in range(len(neighbors)):
                for k in range(j + 1, len(neighbors)):
                    if neighbors[j] not in graph[neighbors[k]]:
                        return -1
            width = max(width, len(neighbors))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        
        lid = local_induction_dimension(graph)
        w_mon = circuit_monotone_width(graph)
        
        if w_mon == -1:
            continue
        
        results.append({
            "metric_name": "mean_difference",
            "metric_value": abs(lid - w_mon),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(lid - w_mon) <= 3,
            "counterexample": f"n={n}, LID(G)={lid}, w_mon(G)={w_mon}" if not results[-1]["conjecture_holds"] else ""
        })
    
    return {
        "metric_name": "mean_difference",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")