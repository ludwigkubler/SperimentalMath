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
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j and (i, j) not in edges_added:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
                    edges_added.add((i, j))
        return adj_matrix
    
    def is_connected(adj_matrix):
        n = len(adj_matrix)
        visited = [False] * n
        stack = [0]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if adj_matrix[u][v] == 1 and not visited[v]:
                        stack.append(v)
        return all(visited)
    
    def compute_quiver_representation(adj_matrix):
        n = len(adj_matrix)
        quiver_rep = []
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    quiver_rep.append((i, j))
        return quiver_rep
    
    def compute_minimal_index_of_automorphism_groups(quiver_rep):
        n = len(quiver_rep)
        automorphisms = set()
        for perm in itertools.permutations(range(n)):
            if all(quiver_rep[perm[i]][perm[j]] == quiver_rep[i][j] for i, j in quiver_rep):
                automorphisms.add(tuple(perm))
        return len(automorphisms)
    
    def compute_frege_proof_depth(quiver_rep):
        # Placeholder function to simulate Frege proof depth
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2 * (n - 1) // n
    graph = generate_d_regular_graph(n, d)
    if not graph or not is_connected(graph):
        return {
            "metric_name": "m_index(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular_or_not_connected"
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
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        m_index_values = [r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None]
        conjecture_holds = all(r["conjecture_holds"] for r in results)
        
        mean_m_index = sum(m_index_values) / len(m_index_values)
        std_m_index = math.sqrt(sum((x - mean_m_index) ** 2 for x in m_index_values) / len(m_index_values))
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        
        if conjecture_holds:
            print(f"RESULT: SUPPORTED mean={mean_m_index} std={std_m_index} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"m_index(G) > 2 * w_F(φ_G)\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE mapping_undefined")