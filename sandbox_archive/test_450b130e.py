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
    
    def generate_dnf(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_cnf(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_block_xor(n):
        k = math.ceil(math.sqrt(n))
        blocks = [generate_dnf(k) for _ in range(k)]
        block_outputs = [sum(blocks[i][j] for i in range(k)) % 2 for j in range(k)]
        return sum(block_outputs[j] * (1 << j) for j in range(k))
    
    def support(g, n):
        return ''.join('1' if g[i] == 1 else '0' for i in range(n))
    
    def build_bipartite_graph(C, n):
        G = [[False] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if support(i, n).issubset(support(j, n)):
                    G[i][j] = True
        return G
    
    def hopcroft_karp(G, n):
        M = [-1] * (2**n)
        dist = [float('inf')] * (2**n)
        
        def bfs():
            queue = []
            for u in range(2**n):
                if M[u] == -1:
                    dist[u] = 0
                    queue.append(u)
                else:
                    dist[u] = float('inf')
            dist[-1] = float('inf')
            while queue:
                u = queue.pop(0)
                if dist[u] < dist[-1]:
                    for v in range(2**n):
                        if G[u][v] and dist[v] == float('inf'):
                            dist[v] = dist[u] + 1
                            queue.append(v)
            return dist[-1] != float('inf')
        
        def dfs(u, visited):
            if u == -1:
                return True
            for v in range(2**n):
                if G[u][v] and not visited[v] and dist[v] == dist[u] + 1:
                    visited[v] = True
                    if dfs(M[v], visited) or M[v] == -1:
                        M[v] = u
                        M[u] = v
                        return True
            dist[u] = float('inf')
            return False
        
        max_matching = 0
        while bfs():
            for u in range(2**n):
                if M[u] == -1:
                    visited = [False] * (2**n)
                    dfs(u, visited)
                    max_matching += 1
        return max_matching
    
    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        size = 2**(n-1) + n
        C2_DNF = generate_dnf(n)
        C2_CNF = generate_cnf(n)
        C4_blockXOR = generate_block_xor(n)
        
        for C, name in [(C2_DNF, 'C2_DNF'), (C2_CNF, 'C2_CNF'), (C4_blockXOR, 'C4_blockXOR')]:
            size += random.randint(0, size // 2)
            G = build_bipartite_graph(C, n)
            mu_B = hopcroft_karp(G, n)
            w_C = len(C) - mu_B
            results.append({
                "metric_name": "w(C)/log_2(size(C))",
                "metric_value": w_C / math.log2(size),
                "instances_tested": 1,
                "conjecture_holds": False if w_C / math.log2(size) < 0.4 else True,
                "counterexample": f"{name} with n={n}, size={size}, w(C)={w_C}"
            })
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        result = "SUPPORTED"
    elif any(r['metric_value'] < 0.4 for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if r['metric_value'] < 0.4)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE"
    
    return {
        "seed": seed,
        "mean_value": mean_value,
        "support_fraction": support_fraction,
        "result": result
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + i for i in range(5, 8)]
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")