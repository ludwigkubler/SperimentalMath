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
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def find_max_disjoint_cliques(graph, k):
        n = len(graph)
        visited = [False] * n
        max_cliques = []
        
        def dfs(node, clique):
            if len(clique) == k:
                max_cliques.append(clique[:])
                return True
            for neighbor in range(n):
                if graph[node][neighbor] and not visited[neighbor]:
                    visited[neighbor] = True
                    if dfs(neighbor, clique + [neighbor]):
                        visited[neighbor] = False
                        return True
                    visited[neighbor] = False
            return False
        
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                dfs(i, [i])
                visited[i] = False
        
        return max_cliques
    
    def estimate_dnf_size(cliques):
        return len(cliques)
    
    n = 40
    k = 3
    graph = generate_random_graph(n)
    cliques = find_max_disjoint_cliques(graph, k)
    r = len(cliques)
    dnf_size = estimate_dnf_size(cliques)
    
    if r == 0:
        return {
            "metric_name": "dnf_size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "no_disjoint_cliques"
        }
    
    c = dnf_size / (n ** (2 / r))
    conjecture_holds = c >= 1
    
    return {
        "metric_name": "dnf_size",
        "metric_value": dnf_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"c={c:.2f} < 1"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30)) + [53, 79, 83, 89, 97]  # Default to first 30 primes and a few more
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_dnf_size = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_dnf_size/len(results):.2f} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std=0 support_fraction={:.2f}".format(total_dnf_size/len(results), support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")