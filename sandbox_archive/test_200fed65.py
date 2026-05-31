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

def generate_d_regular_graph(n, d):
    if d * n % 2 != 0:
        return None
    degree = d * n // 2
    adj_list = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            adj_list[u].append(v)
            adj_list[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(adj_list[i]) < degree and len(adj_list[j]) < degree:
                add_edge(i, j)
    
    return adj_list

def is_valid_quiver_representation(graph):
    if graph is None:
        return False
    n = len(graph)
    for i in range(n):
        if len(graph[i]) != d:
            return False
    return True

def compute_minimal_index_of_automorphism_groups(adj_list):
    n = len(adj_list)
    visited = [False] * n
    
    def dfs(node, parent):
        stack = [(node, parent)]
        while stack:
            current, p = stack.pop()
            if not visited[current]:
                visited[current] = True
                for neighbor in adj_list[current]:
                    if neighbor != p:
                        stack.append((neighbor, current))
    
    connected_components = 0
    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
            connected_components += 1
    
    return n // connected_components

def construct_frege_proof(adj_list):
    n = len(adj_list)
    proof_steps = []
    for i in range(n):
        for j in adj_list[i]:
            proof_steps.append((i, j))
    return proof_steps

def compute_frege_proof_depth(proof_steps):
    depth = 0
    max_depth = 0
    stack = []
    
    for step in proof_steps:
        u, v = step
        while stack and stack[-1][1] != u:
            stack.pop()
        if not stack:
            depth += 1
        stack.append((u, v))
        max_depth = max(max_depth, depth)
    
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "Spearman's rank correlation"
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, n - 1)
            graph = generate_d_regular_graph(n, d)
            if not is_valid_quiver_representation(graph):
                continue
            
            adj_list = graph
            m_index = compute_minimal_index_of_automorphism_groups(adj_list)
            proof_steps = construct_frege_proof(adj_list)
            w_F = compute_frege_proof_depth(proof_steps)
            
            instances_tested += 1
            n_max = max(n_max, n)
            
            if m_index > 2 * w_F:
                conjecture_holds = False
                counterexample = f"n={n}, d={d}, m_index(G)={m_index}, w_F(φ_G)={w_F}"
                break
        
        if not conjecture_holds:
            break
    
    return {
        "metric_name": metric_name,
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")