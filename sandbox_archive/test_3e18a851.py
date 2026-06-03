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
    
    def generate_k_regular_graph(k, n):
        if k * (k - 1) // 2 >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < k and len(graph[j]) < k:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def girth(graph):
        n = len(graph)
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        queue = []
        for i in range(n):
            queue.append((i, 1))
        while queue:
            u, d = queue.pop(0)
            if dist[u][u] < d:
                continue
            for v in graph[u]:
                if dist[u][v] > d + 1:
                    dist[u][v] = d + 1
                    queue.append((v, d + 1))
        return min(max(row) for row in dist)
    
    def persistent_homology(graph):
        n = len(graph)
        simplicial_complex = []
        for i in range(n):
            simplicial_complex.append([i])
        for k in range(2, n):
            new_simplices = []
            for simplex in simplicial_complex:
                for j in range(len(simplex)):
                    new_simplex = simplex[:j] + simplex[j+1:]
                    if len(new_simplex) == k and all(graph[new_simplex[i]][new_simplex[j]] for i, j in itertools.combinations(range(k), 2)):
                        new_simplices.append(new_simplex)
            simplicial_complex.extend(new_simplices)
        return len(simplicial_complex)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if len(neighbors.intersection(set(graph[j]))) == k - 1:
                    rank += 1
        return rank
    
    def mli(simplicial_complex):
        n = len(simplicial_complex)
        lcoh = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if set(simplicial_complex[i]).issubset(set(simplicial_complex[j])):
                    lcoh[j] += 1
        return max(lcoh) - min(lcoh)
    
    k = random.randint(3, 5)
    n = random.randint(k * (k + 1), 40)
    graph = generate_k_regular_graph(k, n)
    if not graph:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_k_regular"
        }
    
    if girth(graph) <= k + 2:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "girth_not_greater_than_k_plus_2"
        }
    
    simplicial_complex = persistent_homology(graph)
    mli_value = mli(simplicial_complex)
    r_value = communication_complexity_rank(graph)
    
    if mli_value is None or r_value is None:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "computation_failed"
        }
    
    if mli_value != r_value:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"mli(G) != r(G): {mli_value} != {r_value}"
        }
    
    if r_value < 2 * k - 4:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"r(G) < 2k - 4: {r_value} < {2 * k - 4}"
        }
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"mli(G) != r(G)\" first_failing_seed={first_failing_seed}"
    
    print(result)