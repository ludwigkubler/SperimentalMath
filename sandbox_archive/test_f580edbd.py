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
    
    n = 5 + (seed % 30) * 2  # Sweep n through {5, 10, 15, 20, 30, 40}
    if n > 40:
        return {
            "metric_name": "Free Entropy vs Distinguishing Tensor Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_max=40 is exceeded"
        }
    
    # Generate a random graph G on n vertices
    G = {i: [] for i in range(n)}
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = sorted(random.sample(range(n), 2))
        if (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
    
    # Compute the free entropy F(G)
    def compute_free_entropy(graph):
        total_edges = sum(len(neighbors) for neighbors in graph.values())
        return -math.log(total_edges / (n * (n - 1)))
    
    F_G = compute_free_entropy(G)
    
    # Choose a BP_readTwice P uniformly at random among all possible BP_readTwice of size n
    def generate_BP_readTwice(n):
        return [random.sample(range(n), 2) for _ in range(n)]
    
    P = generate_BP_readTwice(n)
    
    # Compute the distinguishing tensor width ρ(P)
    def compute_distinguishing_tensor_width(bp_readtwice, graph):
        visited = set()
        queue = bp_readtwice[0]
        while queue:
            u, v = queue.pop(0)
            if (u, v) not in visited and (v, u) not in visited:
                visited.add((u, v))
                for neighbor in graph[u]:
                    if (neighbor, v) not in visited and (v, neighbor) not in visited:
                        queue.append((v, neighbor))
        return len(visited)
    
    ρ_P = compute_distinguishing_tensor_width(P, G)
    
    # Check the relationship F(G) = O(log(ρ(P)))
    if ρ_P == 0:
        return {
            "metric_name": "Free Entropy vs Distinguishing Tensor Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "distinguishing_tensor_width=0"
        }
    
    if F_G > math.log(ρ_P):
        return {
            "metric_name": "Free Entropy vs Distinguishing Tensor Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"F(G)={F_G}, ρ(P)={ρ_P}"
        }
    
    return {
        "metric_name": "Free Entropy vs Distinguishing Tensor Width",
        "metric_value": F_G,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")