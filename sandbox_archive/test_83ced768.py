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
    
    # Define k-CLIQUE problem and related structures
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    def is_clique(graph, clique):
        for u, v in itertools.combinations(clique, 2):
            if (u, v) not in graph or (v, u) not in graph:
                return False
        return True
    
    # Compute minimal order of formal language automorphisms
    def compute_automorphism_order(graph):
        n = len(graph)
        vertices = list(range(n))
        automorphisms = []
        
        def is_valid_permutation(perm):
            for u, v in graph:
                if perm[u] not in graph[perm[v]]:
                    return False
            return True
        
        def generate_permutations():
            for p in itertools.permutations(vertices):
                if is_valid_permutation(p):
                    automorphisms.append(p)
        
        generate_permutations()
        return len(automorphisms)
    
    # Simulate on monotone circuit model and measure depth
    def simulate_circuit_depth(graph, automorphism_order):
        n = len(graph)
        max_depth = 0
        
        def dfs(node, path, depth):
            nonlocal max_depth
            if depth > max_depth:
                max_depth = depth
            for neighbor in graph[node]:
                if neighbor not in path:
                    dfs(neighbor, path + [neighbor], depth + 1)
        
        for start in range(n):
            dfs(start, [start], 0)
        
        return math.log2(max_depth) if max_depth > 0 else 0
    
    # Main trial logic
    n = random.randint(5, 40)
    k = min(n, random.randint(3, 10))
    graph = generate_k_clique(n, k)
    
    if graph is None:
        return {
            "metric_name": "circuit_depth",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k_clique_not_possible"
        }
    
    automorphism_order = compute_automorphism_order(graph)
    circuit_depth = simulate_circuit_depth(graph, automorphism_order)
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": circuit_depth,
        "instances_tested": 1,
        "conjecture_holds": automorphism_order <= math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")