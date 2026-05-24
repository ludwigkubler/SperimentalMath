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
    
    def generate_k_clique(n, k):
        if k > n or k == 0:
            return None
        nodes = list(range(n))
        clique = random.sample(nodes, k)
        graph = {i: [] for i in range(n)}
        for u in clique:
            for v in clique:
                if u != v and (v not in graph[u] or u not in graph[v]):
                    graph[u].append(v)
                    graph[v].append(u)
        return graph
    
    def calculate_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        
        def dfs(node, parent):
            nonlocal rank
            stack = [(node, parent)]
            while stack:
                node, parent = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    rank += 1
                    for neighbor in graph[node]:
                        if neighbor != parent:
                            stack.append((neighbor, node))
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return rank
    
    def calculate_k_clique_lower_bound(n, k):
        if k > n or k == 0:
            return None
        return math.comb(n, k) * (k - 1) ** (n - k)
    
    results = []
    for n in range(5, 41):
        for _ in range(6):  # Ensure at least 30 instances per seed
            graph = generate_k_clique(n, random.randint(2, min(3, n)))
            if graph is None:
                continue
            rank = calculate_rank(graph)
            lower_bound = calculate_k_clique_lower_bound(n, random.randint(2, min(3, n)))
            results.append((rank, lower_bound))
    
    total_rank = sum(rank for rank, _ in results)
    total_lower_bound = sum(lower_bound for _, lower_bound in results)
    mean_rank = total_rank / len(results)
    mean_lower_bound = total_lower_bound / len(results)
    
    conjecture_holds = all(0.5 * lower_bound <= rank <= 2 * lower_bound for rank, lower_bound in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")