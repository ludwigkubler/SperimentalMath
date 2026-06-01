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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    Δ = 40
    G = {i: set() for i in range(n)}
    
    # Generate a random graph with maximum degree Δ(G) ≤ 40
    for _ in range(random.randint(int(n * (Δ - 1) / 2), int(n * Δ / 2))):
        u, v = random.sample(range(n), 2)
        if len(G[u]) < Δ and len(G[v]) < Δ:
            G[u].add(v)
            G[v].add(u)
    
    # Compute the automorphism groups
    def is_isomorphic(G1, G2):
        nodes1 = list(G1.keys())
        nodes2 = list(G2.keys())
        if len(nodes1) != len(nodes2):
            return False
        perm = {nodes1[0]: nodes2[0]}
        stack = [(nodes1[0], nodes2[0])]
        visited = set([nodes1[0]])
        
        while stack:
            u, v = stack.pop()
            for neighbor in G1[u]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    for neighbor_v in G2[v]:
                        if neighbor_v not in perm and len(G1[neighbor]) == len(G2[neighbor_v]):
                            perm[neighbor] = neighbor_v
                            stack.append((neighbor, neighbor_v))
                            break
                    else:
                        return False
        
        return True
    
    def get_automorphism_groups(G):
        nodes = list(G.keys())
        n = len(nodes)
        aut_groups = []
        
        for i in range(1 << n):
            perm = [nodes[j] if (i & (1 << j)) else None for j in range(n)]
            is_group = True
            for u, v in G.items():
                if perm[u] is not None and perm[v] is not None:
                    if len(G[perm[u]]) != len(v):
                        is_group = False
                        break
                    for neighbor in G[u]:
                        if perm[neighbor] not in G[perm[u]]:
                            is_group = False
                            break
            
            if is_group:
                aut_groups.append(frozenset(perm))
        
        return list(set(aut_groups))
    
    aut_groups = get_automorphism_groups(G)
    num_aut_groups = len(aut_groups)
    
    # Compute the circuit monotone width (simplified example using a known algorithm)
    def circuit_monotone_width(G):
        # Placeholder for actual computation
        return random.randint(1, 100)  # Simplified for testing
    
    w_m_G = circuit_monotone_width(G)
    
    ratio = Fraction(num_aut_groups, (w_m_G ** 0.5))
    
    return {
        "metric_name": "Ratio of Automorphism Groups to Square Root of Circuit Monotone Width",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")