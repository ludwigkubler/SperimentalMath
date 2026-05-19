# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def build_dnf(n):
    return [random.choice([0, 1]) for _ in range(2**(n-1))] + [random.randint(0, n) for _ in range(n)]

def build_cnf(n):
    return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**(n-1))]

def build_block_xor(n):
    block_size = int(n**0.5)
    blocks = [build_dnf(block_size) for _ in range(block_size)]
    result = []
    for i in range(2**(block_size)):
        block_output = 0
        for j in range(block_size):
            if blocks[j][i % block_size] == 1:
                block_output ^= 1
        result.append(block_output)
    return result

def support(gate, assignments):
    return [i for i, bit in enumerate(assignments) if gate[i] == 1]

def build_bipartite_graph(C, assignments):
    G = []
    for g in C:
        G.extend([(g, h) for h in C if set(support(g, assignments)) <= set(support(h, assignments))])
    return G

def hopcroft_karp(G):
    n = len(G)
    U = set(range(n // 2))
    V = set(range(n // 2, n))
    match = [-1] * n
    dist = [0] * n
    
    def bfs():
        queue = []
        for u in U:
            if match[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        dist[float('inf')] = float('inf')
        while queue:
            u = queue.pop(0)
            if dist[u] < dist[float('inf')]:
                for v in V:
                    if (u, v) in G and dist[v] == float('inf'):
                        dist[v] = dist[u] + 1
                        queue.append(v)
        return dist[float('inf')] != float('inf')
    
    def dfs(u):
        if u in U:
            for v in V:
                if (u, v) in G and dist[v] == dist[u] + 1:
                    dist[v] = float('inf')
                    if match[v] == -1 or dfs(match[v]):
                        match[u] = v
                        match[v] = u
                        return True
            return False
        else:
            for (u, v) in G:
                if u == u and dist[v] == dist[u] + 1:
                    dist[v] = float('inf')
                    if dfs(v):
                        return True
            return False
    
    while bfs():
        for u in U:
            if match[u] == -1 and dfs(u):
                pass
    
    return sum(1 for u in U if match[u] != -1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        C_dnf = build_dnf(n)
        C_cnf = build_cnf(n)
        C_block_xor = build_block_xor(n)
        
        assignments = [random.randint(0, 1) for _ in range(n)]
        
        for C in [C_dnf, C_cnf, C_block_xor]:
            size_C = len(C)
            w_C = hopcroft_karp(build_bipartite_graph(C, assignments))
            ratio = Fraction(w_C, n).limit_denominator()
            results.append({"n": n, "size": size_C, "w_C": w_C, "ratio": ratio})
    
    min_ratio = min(result["ratio"] for result in results)
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    
    conjecture_holds = min_ratio >= Fraction(2, 5) and mean_ratio >= Fraction(1, 2)
    counterexample = "" if conjecture_holds else "min_ratio < 0.4"
    
    return {
        "metric_name": "w(C)/log_2(size(C))",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    ratios = [result["ratio"] for result in results]
    min_ratio = min(ratios)
    mean_ratio = sum(ratios) / len(ratios)
    
    if all(r >= Fraction(2, 5) for r in ratios):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif any(r < Fraction(2, 5) for r in ratios):
        first_failing_seed = seeds[ratios.index(min(ratios))]
        print(f"RESULT: FALSIFIED counterexample='min_ratio < 0.4' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")