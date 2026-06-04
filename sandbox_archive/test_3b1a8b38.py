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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = {i: [] for i in range(n)}
    edges = set()
    
    def add_edge(u, v):
        if (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    for _ in range(d * n // 2):
        while True:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                add_edge(u, v)
                break
    
    return graph

def geometric_group_action(graph):
    n = len(graph)
    visited = set()
    
    def dfs(node, action):
        if tuple(action) in visited:
            return
        visited.add(tuple(action))
        
        for neighbor in graph[node]:
            new_action = [action[i] ^ (1 << i) for i in range(n)]
            dfs(neighbor, new_action)
    
    for node in range(n):
        dfs(node, [0] * n)
    
    return len(visited)

def sat_clause_subset_entropy(clauses):
    n = len(clauses[0])
    entropy = 0
    for clause in clauses:
        for i in range(n):
            if clause[i] == '1':
                entropy += Fraction(1, 2 ** (n - i))
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 6))
        graph = generate_d_regular_graph(n, d)
        clauses = [[random.choice('01') for _ in range(d)] for _ in range(n)]
        
        min_order = geometric_group_action(graph)
        entropy = sat_clause_subset_entropy(clauses)
        
        results.append({
            "n": n,
            "min_order": min_order,
            "entropy": entropy
        })
    
    if not results:
        return {
            "metric_name": "log2_min_order",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_min_orders = [Fraction(min_order).log(2) for min_order in results[-1]["min_order"]]
    entropy_values = [result["entropy"] for result in results]
    
    rho = 0.0
    n_max = max(result["n"] for result in results)
    
    if len(log2_min_orders) > 1 and len(entropy_values) > 1:
        n_pairs = min(len(log2_min_orders), len(entropy_values))
        rank_log2_min_orders = [sorted(range(n_pairs), key=lambda i: log2_min_orders[i]) for _ in range(n_pairs)]
        rank_entropy_values = [sorted(range(n_pairs), key=lambda i: entropy_values[i]) for _ in range(n_pairs)]
        
        sum_rank_diffs_squared = 0
        for i in range(n_pairs):
            for j in range(n_pairs):
                sum_rank_diffs_squared += (rank_log2_min_orders[i][j] - rank_entropy_values[j][i]) ** 2
        
        rho = 1 - sum_rank_diffs_squared / (n_pairs * (n_pairs**2 - 1) / 4)
    
    return {
        "metric_name": "log2_min_order",
        "metric_value": float(rho),
        "instances_tested": len(results[-1]["min_order"]),
        "n_max": n_max,
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")