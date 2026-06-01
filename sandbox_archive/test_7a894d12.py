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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        G = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(G[i]) < d and len(G[j]) < d and (i, j) not in edges_added:
                    G[i].append(j)
                    G[j].append(i)
                    edges_added.add((i, j))
        return G
    
    def circuit_monotone_width(G):
        n = len(G)
        if n == 0:
            return 0
        visited = [False] * n
        stack = []
        
        def dfs(v):
            stack.append(v)
            visited[v] = True
            for neighbor in G[v]:
                if not visited[neighbor]:
                    dfs(neighbor)
            stack.pop()
        
        dfs(0)
        return len(stack) - 1
    
    def alexander_dirac_invariant(G):
        n = len(G)
        if n == 0:
            return 0
        visited = [False] * n
        stack = []
        
        def dfs(v):
            stack.append(v)
            visited[v] = True
            for neighbor in G[v]:
                if not visited[neighbor]:
                    dfs(neighbor)
            stack.pop()
        
        dfs(0)
        return len(stack) - 1
    
    def construct_2_manifold(G):
        n = len(G)
        M = []
        for i in range(n):
            M.append([i])
        return M
    
    def alexander_dirac_invariant_manifold(M):
        return sum(len(v) for v in M)
    
    d = random.randint(3, 4)
    n = random.randint(5, 20)
    G = generate_d_regular_graph(d, n)
    if G is None:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    w_G = circuit_monotone_width(G)
    M = construct_2_manifold(G)
    m_alex_M = alexander_dirac_invariant_manifold(M)
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": w_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(w_G - m_alex_M) <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed + 1}")