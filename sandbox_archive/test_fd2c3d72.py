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
    
    def generate_d_regular_graph(d, n):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def geometric_group_action(graph):
        n = len(graph)
        min_order = float('inf')
        for i in range(n):
            action = [graph[(i + j) % n] for j in range(n)]
            order = 1
            visited = set()
            while tuple(action) not in visited:
                visited.add(tuple(action))
                action = [graph[(action[j][k] + j) % n] for k in range(len(action))]
                order += 1
            min_order = min(min_order, order)
        return min_order
    
    def sat_clause_subset_entropy(clauses):
        num_clauses = len(clauses)
        total_literals = sum(len(c) for c in clauses)
        entropy = 0
        for i in range(2 ** total_literals):
            count = 0
            for clause in clauses:
                if all((i >> (total_literals - l - 1)) & 1 == literal for l, literal in enumerate(clause)):
                    count += 1
            if count > 0:
                p = count / num_clauses
                entropy -= p * math.log2(p)
        return entropy
    
    def generate_sat_instance(d, n):
        clauses = []
        for i in range(n):
            clause = random.sample(range(1, d+1), random.randint(1, d))
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(d=3, n=n)  # Example degree 3
        if graph is None:
            continue
        clauses = generate_sat_instance(d=3, n=n)
        min_order = geometric_group_action(graph)
        entropy = sat_clause_subset_entropy(clauses)
        results.append((min_order, entropy))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def spearman_rank_correlation(data):
        ranks = {x: rank for rank, x in enumerate(sorted(set(x[0] for x in data)), start=1)}
        ranked_data = [(ranks[x], y) for x, y in data]
        sorted_data = sorted(ranked_data)
        n = len(sorted_data)
        sum_d_squared = sum((i - (n + 1) / 2) ** 2 for i, _ in enumerate(sorted_data))
        rho = 1 - 6 * sum_d_squared / (n * (n**2 - 1))
        return rho
    
    rho = spearman_rank_correlation(results)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.4 < rho <= 0.7,
        "counterexample": "" if 0.4 < rho <= 0.7 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_rho} std=NA support_fraction={support_fraction}"
    elif any(r["counterexample"] == "not_enough_instances" for r in results):
        result = "INCONCLUSIVE not_enough_instances"
    else:
        rho_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
        mean_rho = sum(rho_values) / len(rho_values)
        support_fraction = len(rho_values) / len(results)
        result = f"FALSIFIED counterexample=NA first_failing_seed={min(seed for seed, r in enumerate(results) if not r['conjecture_holds'])}"
    
    print(result)