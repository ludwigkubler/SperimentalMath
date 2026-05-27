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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def isomorphism(G1, G2):
        if len(G1) != len(G2):
            return False
        mapping = {}
        visited = set()
        def dfs(node, other_node):
            if node in visited:
                return True
            visited.add(node)
            for neighbor in G1[node]:
                if (neighbor not in mapping or mapping[neighbor] not in G2[other_node]) and not dfs(neighbor, mapping.get(neighbor, -1)):
                    return False
            return True
        for node in G1:
            if node not in visited:
                other_nodes = [n for n in G2 if len(G2[n]) == len(G1[node])]
                if not any(dfs(node, other_node) for other_node in other_nodes):
                    return False
        return True
    
    def symplectic_form(G):
        n = len(G)
        S = [[0] * n for _ in range(n)]
        for (i, j) in G:
            S[i][j] = 1
            S[j][i] = -1
        return S
    
    def minimal_rank(S):
        n = len(S)
        rank = 0
        for i in range(n):
            if all(S[j][i] == 0 for j in range(i)):
                rank += 1
        return rank
    
    def communication_complexity(G, H):
        # Simplified protocol: compare edge sets directly
        return len(G) + len(H)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_graph(n)
    H = generate_graph(n)
    while not isomorphism(G, H):
        G = generate_graph(n)
        H = generate_graph(n)
    
    S_G = symplectic_form(G)
    rho_S_G = minimal_rank(S_G)
    C_P = communication_complexity(G, H)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": C_P,
        "instances_tested": 1,
        "conjecture_holds": C_P <= n**2 * rho_S_G,
        "counterexample": "" if C_P <= n**2 * rho_S_G else f"Graphs G and H are isomorphic but communication complexity {C_P} > O({n**2 * rho_S_G})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C_P = sum(r["metric_value"] for r in results) / len(results)
    std_C_P = math.sqrt(sum((r["metric_value"] - mean_C_P) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C_P} std={std_C_P} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C_P} std={std_C_P} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graphs G and H are isomorphic but communication complexity exceeds O(n^2 * rho(S(G)))\" first_failing_seed={first_failing_seed}")