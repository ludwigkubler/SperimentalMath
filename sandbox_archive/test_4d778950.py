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
        adj_list = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(adj_list[i]) < d and len(adj_list[j]) < d:
                    edge = (i, j)
                    reverse_edge = (j, i)
                    if edge not in edges_added and reverse_edge not in edges_added:
                        adj_list[i].append(j)
                        adj_list[j].append(i)
                        edges_added.add(edge)
                        edges_added.add(reverse_edge)
        return adj_list
    
    def is_valid_quiver_representation(adj_list):
        n = len(adj_list)
        for i in range(n):
            if len(adj_list[i]) % 2 != 0:
                return False
        return True
    
    def compute_minimal_index_of_automorphism_groups(adj_list):
        n = len(adj_list)
        visited = [False] * n
        min_index = float('inf')
        
        def dfs(node, parent, path):
            nonlocal min_index
            if node in path:
                cycle_length = len(path) - path.index(node)
                min_index = min(min_index, cycle_length)
                return
            visited[node] = True
            path.append(node)
            for neighbor in adj_list[node]:
                if neighbor != parent:
                    dfs(neighbor, node, path)
            path.pop()
            visited[node] = False
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1, [])
        
        return min_index
    
    def compute_frege_proof_depth(adj_list):
        n = len(adj_list)
        max_depth = 0
        stack = [(i, 0) for i in range(n)]
        
        while stack:
            node, depth = stack.pop()
            if depth > max_depth:
                max_depth = depth
            for neighbor in adj_list[node]:
                stack.append((neighbor, depth + 1))
        
        return max_depth
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    
    if not is_valid_quiver_representation(graph):
        return {
            "metric_name": "m_index(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_index = compute_minimal_index_of_automorphism_groups(graph)
    frege_depth = compute_frege_proof_depth(graph)
    
    if m_index > 2 * frege_depth:
        return {
            "metric_name": "m_index(G)",
            "metric_value": m_index,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"m_index({m_index}) > 2 * w_F({frege_depth})"
        }
    
    return {
        "metric_name": "m_index(G)",
        "metric_value": m_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_m_index = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_m_index) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_m_index} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_index(G) > 2 * w_F(φ_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")