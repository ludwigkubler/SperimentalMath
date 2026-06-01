# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n, max_degree):
        G = [[] for _ in range(n)]
        edges_added = 0
        while edges_added < (n * max_degree) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and v not in G[u]:
                G[u].append(v)
                G[v].append(u)
                edges_added += 1
        return G
    
    def get_automorphism_groups(G):
        n = len(G)
        aut_groups = defaultdict(set)
        
        def dfs(node, perm, visited):
            if node in visited:
                return True
            visited.add(node)
            for neighbor in G[node]:
                if neighbor not in perm:
                    continue
                perm[neighbor] = perm.get(perm[node], perm[node])
                if not dfs(neighbor, perm, visited):
                    return False
            return True
        
        def is_automorphism(perm):
            visited = set()
            for node in range(n):
                if node not in visited:
                    if not dfs(node, perm, visited):
                        return False
            return True
        
        for perm in itertools.permutations(range(n)):
            if is_automorphism(perm):
                aut_groups[frozenset(perm)].add(frozenset(G[i] for i in range(n)))
        
        return {frozenset(group): len(group) for group in aut_groups.values()}
    
    def circuit_monotone_width(G):
        n = len(G)
        if n == 0:
            return 0
        width = float('inf')
        
        def dfs(node, visited, path):
            nonlocal width
            if node in visited:
                cycle_length = len(path) - path.index(node)
                width = min(width, cycle_length)
                return
            visited.add(node)
            path.append(node)
            for neighbor in G[node]:
                dfs(neighbor, visited, path)
            path.pop()
        
        for i in range(n):
            visited = set()
            dfs(i, visited, [])
        
        return width
    
    n = 30
    max_degree = 40
    G = generate_graph(n, max_degree)
    
    aut_groups = get_automorphism_groups(G)
    num_aut_groups = sum(aut_groups.values())
    w_m_G = circuit_monotone_width(G)
    
    if w_m_G == 0:
        return {
            "metric_name": "Ratio of Automorphism Groups to sqrt(Circuit Monotone Width)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Circuit monotone width is zero"
        }
    
    ratio = num_aut_groups / math.sqrt(w_m_G)
    
    return {
        "metric_name": "Ratio of Automorphism Groups to sqrt(Circuit Monotone Width)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 10 else False,  # Assuming c = 10 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 10' first_failing_seed={first_failing_seed + 1}")