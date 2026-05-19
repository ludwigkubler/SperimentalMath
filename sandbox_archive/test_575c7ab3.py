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
    
    def build_dnf(n):
        return [random.choice([0, 1]) for _ in range(2**(n-1)) + n]
    
    def build_cnf(n):
        return [random.choice([0, 1]) for _ in range(2**(n-1)) + n]
    
    def build_block_xor(n):
        block_size = int(math.ceil(math.sqrt(n)))
        blocks = [build_dnf(block_size) for _ in range(block_size)]
        result = []
        for i in range(n):
            xor_val = 0
            for j in range(block_size):
                if (i // block_size == j):
                    xor_val ^= blocks[j][i % block_size]
            result.append(xor_val)
        return result
    
    def add_padding(gate, padding):
        gate += [0] * padding
        return gate
    
    def support(gate, n):
        return ''.join('1' if gate[i] == 1 else '0' for i in range(n))
    
    def build_bipartite_graph(C, n):
        G = defaultdict(list)
        for i in range(len(C)):
            for j in range(i + 1, len(C)):
                if support(C[i], n) <= support(C[j], n):
                    G[i].append(j)
                    G[j].append(i)
        return G
    
    def hopcroft_karp(G):
        V = set()
        for u in G:
            V.update(G[u])
        V = list(V)
        
        def bfs():
            dist = {u: float('inf') for u in V}
            queue = []
            for u in V:
                if not G[u]:
                    dist[u] = 0
                    queue.append(u)
            while queue:
                u = queue.pop(0)
                for v in G[u]:
                    if dist[v] == float('inf'):
                        dist[v] = dist[u] + 1
                        queue.append(v)
            return dist
        
        def dfs(u, dist):
            if u not in V:
                return True
            for v in G[u]:
                if dist[v] == dist[u] + 1 and dfs(v, dist):
                    G[u].remove(v)
                    G[v].remove(u)
                    return True
            dist[u] = float('inf')
            return False
        
        matching = {}
        while True:
            dist = bfs()
            if all(dist[u] != float('inf') for u in V):
                break
            for u in V:
                if u not in matching and dfs(u, dist):
                    matching[u] = G[u][0]
                    matching[G[u][0]] = u
        
        return len(matching)
    
    n_values = [8, 10, 12, 14]
    results = []
    for n in n_values:
        for _ in range(3):
            C_dnf = build_dnf(n)
            C_cnf = build_cnf(n)
            C_blockxor = build_block_xor(n)
            
            padding = random.randint(0, len(C_dnf) // 2)
            C_dnf = add_padding(C_dnf, padding)
            C_cnf = add_padding(C_cnf, padding)
            C_blockxor = add_padding(C_blockxor, padding)
            
            G_dnf = build_bipartite_graph(C_dnf, n)
            G_cnf = build_bipartite_graph(C_cnf, n)
            G_blockxor = build_bipartite_graph(C_blockxor, n)
            
            w_dnf = hopcroft_karp(G_dnf)
            w_cnf = hopcroft_karp(G_cnf)
            w_blockxor = hopcroft_karp(G_blockxor)
            
            results.append({
                "metric_name": "w(C)/log2(s)",
                "metric_value": w_dnf / math.log2(len(C_dnf)),
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            })
    
    min_ratio = min(r["metric_value"] for r in results)
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    
    if min_ratio >= 0.4 and mean_ratio >= 0.5:
        return {
            "seed": seed,
            "metric_name": "w(C)/log2(s)",
            "metric_value": mean_ratio,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"min_ratio={min_ratio}, mean_ratio={mean_ratio}"
        return {
            "seed": seed,
            "metric_name": "w(C)/log2(s)",
            "metric_value": mean_ratio,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    min_ratio = min(r["metric_value"] for r in results if r["conjecture_holds"])
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min_ratio < 0.4:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_ratio={min_ratio}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")