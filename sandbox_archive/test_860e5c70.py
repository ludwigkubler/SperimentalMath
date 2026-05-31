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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and (u, v) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def compute_quiver_representation(graph):
        n = len(graph)
        quiver_rep = [[0 for _ in range(n)] for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                quiver_rep[u][v] += 1
        return quiver_rep
    
    def compute_minimal_index_of_automorphism_groups(quiver_rep):
        n = len(quiver_rep)
        identity = [1 if i == j else 0 for i in range(n) for j in range(n)]
        automorphisms = []
        
        def is_automorphism(perm):
            permuted_rep = [[quiver_rep[perm[i]][perm[j]] for j in range(n)] for i in range(n)]
            return permuted_rep == quiver_rep
        
        for perm in itertools.permutations(range(n)):
            if is_automorphism(perm):
                automorphisms.append(perm)
        
        min_index = float('inf')
        for u in range(n):
            indices = [i for i, p in enumerate(automorphisms) if p[u] == u]
            min_index = min(min_index, len(indices))
        
        return min_index
    
    def compute_frege_proof_depth(quiver_rep):
        n = len(quiver_rep)
        depth = 0
        stack = [(0, 1)]
        visited = set()
        
        while stack:
            node, level = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in range(n):
                if quiver_rep[node][neighbor] > 0 and neighbor not in visited:
                    stack.append((neighbor, level + 1))
            depth = max(depth, level)
        
        return depth
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "m_index(G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    quiver_rep = compute_quiver_representation(graph)
    m_index_G = compute_minimal_index_of_automorphism_groups(quiver_rep)
    w_F_phi_G = compute_frege_proof_depth(quiver_rep)
    
    return {
        "metric_name": "m_index(G)",
        "metric_value": m_index_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_index_G <= 2 * w_F_phi_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_m_index = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_m_index) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_m_index} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_index(G) > 2 * w_F(φ_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")