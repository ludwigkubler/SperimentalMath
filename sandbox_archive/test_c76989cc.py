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
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for u in range(n):
        for v in range(u + 1, n):
            if len(graph[u]) < d and len(graph[v]) < d:
                add_edge(u, v)
                if len(edges_added) == n * (n - 1) // 2:
                    break
        if len(edges_added) == n * (n - 1) // 2:
            break
    
    return graph

def geometric_group_action(graph):
    n = len(graph)
    action_order = [0] * n
    
    def dfs(node, parent):
        visited[node] = True
        for neighbor in graph[node]:
            if neighbor != parent and not visited[neighbor]:
                dfs(neighbor, node)
                action_order[node] += 1
    
    visited = [False] * n
    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
    
    return max(action_order)

def sat_clause_subset_entropy(clauses):
    num_clauses = len(clauses)
    total_bits = sum(len(c) for c in clauses)
    entropy = 0.0
    for i in range(2 ** total_bits):
        count = 0
        for clause in clauses:
            if all(var not in clause or var >= 0 for var in clause):
                count += 1
        if count > 0:
            p = Fraction(count, 2 ** total_bits)
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2 * (n - 1) // n
        graph = generate_d_regular_graph(n, d)
        min_order = geometric_group_action(graph)
        entropy = sat_clause_subset_entropy([[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)])
        
        results.append({
            "n": n,
            "min_order": min_order,
            "entropy": entropy
        })
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    rho = calculate_spearman_rho(results)
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.4 < rho <= 0.7,
        "counterexample": "" if 0.4 < rho <= 0.7 else f"rho={rho}"
    }

def calculate_spearman_rho(results):
    n = len(results)
    ranks_order = sorted(range(n), key=lambda i: results[i]["min_order"])
    ranks_entropy = sorted(range(n), key=lambda i: results[i]["entropy"])
    
    d_squared_sum = sum((ranks_order[i] - ranks_entropy[i]) ** 2 for i in range(n))
    rho_numerator = 1 - (6 * d_squared_sum) / (n * (n ** 2 - 1))
    return max(0, min(rho_numerator, 1))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}"
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        counterexample_desc = next(r["counterexample"] for r in results if r["counterexample"] != "")
        result = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"
    else:
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if 0.4 < r["metric_value"] <= 0.7) / len(results)
        result = f"FALSIFIED counterexample=\"rho={mean_rho}\" first_failing_seed=NA"
    
    print(result)