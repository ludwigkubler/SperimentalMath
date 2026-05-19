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
        return [random.choice([0, 1]) for _ in range(2**(n-1))]
    
    def build_cnf(n):
        return [random.choice([0, 1]) for _ in range(2**(n-1))]
    
    def build_block_xor(n):
        block_size = int(math.ceil(math.sqrt(n)))
        blocks = [build_dnf(block_size) for _ in range(block_size)]
        result = []
        for i in range(n):
            result.append(any(blocks[j][i // block_size] == 1 for j in range(block_size)))
        return result
    
    def add_subsumed_gates(circuit, num_subsumed):
        n = len(circuit)
        subsumed_indices = random.sample(range(n), num_subsumed)
        new_circuit = [circuit[i] if i not in subsumed_indices else 0 for i in range(n)]
        return new_circuit
    
    def support(gate, n):
        return ''.join('1' if gate[i] == 1 else '0' for i in range(n))
    
    def build_bipartite_graph(circuit, n):
        G = defaultdict(list)
        for i in range(n):
            for j in range(i+1, n):
                if support(i, n) <= support(j, n):
                    G[i].append(j)
                    G[j].append(i)
        return G
    
    def hopcroft_karp(G):
        n = len(G)
        match = [-1] * n
        dist = [0] * n
        
        def bfs():
            Q = []
            for u in range(n):
                if match[u] == -1:
                    dist[u] = 0
                    Q.append(u)
                else:
                    dist[u] = math.inf
            dist[n] = math.inf
            while Q:
                u = Q.pop(0)
                if dist[u] < dist[n]:
                    for v in G[u]:
                        if dist[match[v]] == math.inf:
                            dist[match[v]] = dist[u] + 1
                            Q.append(match[v])
            return dist[n] != math.inf
        
        def dfs(u):
            if u < n:
                for v in G[u]:
                    if dist[v] == dist[u] + 1 and dfs(match[v]):
                        match[u], match[v] = match[v], u
                        return True
                dist[u] = math.inf
                return False
            else:
                return dist[n] != math.inf
        
        while bfs():
            for u in range(n):
                if match[u] == -1 and dfs(u):
                    pass
        return sum(match[i] != -1 for i in range(n)) // 2
    
    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        for _ in range(30):
            circuit_type = random.choice(['DNF', 'CNF', 'BlockXOR'])
            if circuit_type == 'DNF':
                C = build_dnf(n)
            elif circuit_type == 'CNF':
                C = build_cnf(n)
            else:
                C = build_block_xor(n)
            
            num_subsumed = random.randint(0, len(C) // 2)
            C = add_subsumed_gates(C, num_subsumed)
            
            G = build_bipartite_graph(C, n)
            w_C = hopcroft_karp(G)
            size_C = len(C)
            ratio = w_C / math.log2(size_C)
            
            results.append({
                "metric_name": "w(C)/log2(s)",
                "metric_value": ratio,
                "instances_tested": 1,
                "conjecture_holds": ratio >= 0.4,
                "counterexample": ""
            })
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_ratio": mean_ratio,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(result["mean_ratio"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")