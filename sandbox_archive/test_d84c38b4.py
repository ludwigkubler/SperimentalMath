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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_planar_graph(n):
        if n < 3 or n % 2 != 0:
            return None
        G = [[] for _ in range(n)]
        edges = list(combinations(range(n), 2))
        while len(G[0]) < (n - 1) // 2:
            u, v = random.choice(edges)
            if u not in G[v] and v not in G[u]:
                G[u].append(v)
                G[v].append(u)
                edges.remove((u, v))
                edges.remove((v, u))
        return G
    
    def hypercube_representation(G):
        n = len(G)
        H = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if j not in G[i]:
                    H[i].append(j)
                    H[j].append(i)
        return H
    
    def geometric_symmetry_order(H):
        n = len(H)
        order = 0
        for i in range(n):
            visited = [False] * n
            stack = [i]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in H[u]:
                        if not visited[v]:
                            stack.append(v)
            order += 1
        return order
    
    def circuit_monotone_width(G):
        n = len(G)
        width = 0
        for subset in range(1, 2 ** n):
            subset_nodes = [i for i in range(n) if (subset >> i) & 1]
            if all(len(set(G[u] & set(subset_nodes)) | {u} - set(subset_nodes)) == len(set(G[v] & set(subset_nodes)) | {v} - set(subset_nodes))
                   for u, v in combinations(subset_nodes, 2)):
                width = max(width, len(subset_nodes))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_coefficient = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        G = generate_planar_graph(n)
        if G is None:
            continue
        H = hypercube_representation(G)
        if not H:
            continue
        
        order = geometric_symmetry_order(H)
        width = circuit_monotone_width(G)
        
        correlation_coefficient += (order - n) * (width - n) / (n ** 2)
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean = correlation_coefficient / instances_tested
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.9' first_failing_seed={first_failing_seed}")