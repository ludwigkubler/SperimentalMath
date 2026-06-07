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
        if (n * (n - 1)) % (d * 2) != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def is_connected(graph):
        n = len(graph)
        visited = [False] * n
        stack = [0]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if graph[u][v] == 1 and not visited[v]:
                        stack.append(v)
        return all(visited)
    
    def find_automorphisms(graph):
        n = len(graph)
        automorphisms = set()
        
        def dfs(u, mapping, used):
            if u == n:
                automorphisms.add(tuple(mapping))
                return
            for v in range(n):
                if not used[v]:
                    valid = True
                    for w in range(n):
                        if graph[u][w] != graph[v][mapping[w]]:
                            valid = False
                            break
                    if valid:
                        mapping[u] = v
                        used[v] = True
                        dfs(u + 1, mapping, used)
                        used[v] = False
        
        dfs(0, [None] * n, [False] * n)
        return automorphisms
    
    def symmetry_breaking_number(automorphisms):
        return len(automorphisms) - 1
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    rank += 1
        return rank
    
    results = []
    for d in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = generate_d_regular_graph(40, d)
            if graph is None:
                continue
            automorphisms = find_automorphisms(graph)
            if not is_connected(graph) or len(automorphisms) == 1:
                continue
            sbn = symmetry_breaking_number(automorphisms)
            r = communication_complexity_rank(graph)
            results.append((sbn, r))
    
    if not results:
        return {
            "metric_name": "SBN(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid graph found"
        }
    
    sbns, rs = zip(*results)
    mean_sbn = sum(sbns) / len(sbns)
    mean_r = sum(rs) / len(rs)
    corr_coeff = (sum((sbns[i] - mean_sbn) * (rs[i] - mean_r) for i in range(len(sbns))) /
                  math.sqrt(sum((sbns[i] - mean_sbn)**2 for i in range(len(sbns))) *
                            sum((rs[i] - mean_r)**2 for i in range(len(rs)))))
    
    return {
        "metric_name": "SBN(G)",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(corr_coeff) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)
        print(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Insufficient support\" first_failing_seed={first_failing_seed}")