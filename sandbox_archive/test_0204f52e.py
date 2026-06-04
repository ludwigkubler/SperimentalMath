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
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def geometric_group_action(graph):
        n = len(graph)
        min_order = float('inf')
        for i in range(n):
            action = [graph[(i + j) % n] for j in range(n)]
            order = 1
            visited = set()
            while tuple(action[i]) not in visited:
                visited.add(tuple(action[i]))
                action = [graph[(action[i][j] + j) % n] for j in range(n)]
                order += 1
            min_order = min(min_order, order)
        return min_order
    
    def sat_clause_subset_entropy(clauses):
        total_clauses = len(clauses)
        entropy = 0
        for clause in clauses:
            if len(clause) > 0:
                p = Fraction(1, 2 ** len(clause))
                entropy += -p * math.log(p, 2)
        return entropy
    
    def generate_sat_instance(n):
        clauses = []
        for i in range(n):
            variables = random.sample(range(n), n // 2)
            clause = [random.choice([-1, 1]) * var for var in variables]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        clauses = generate_sat_instance(n)
        min_order = geometric_group_action(graph)
        entropy = sat_clause_subset_entropy(clauses)
        results.append({
            "n": n,
            "min_order": min_order,
            "entropy": entropy
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        sum_differences_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_differences_squared) / (n * (n**2 - 1))
    
    x = [result["min_order"] for result in results]
    y = [result["entropy"] for result in results]
    rho = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": rho > 0.7,
        "counterexample": "" if rho > 0.4 else "rho <= 0.4"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    rho_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    support_fraction = sum(1 for rho in rho_values if rho > 0.7) / len(rho_values)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(rho_values)/len(rho_values)} std={math.sqrt(sum((rho - sum(rho_values)/len(rho_values))**2 for rho in rho_values) / len(rho_values))} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False and result["counterexample"] == "rho <= 0.4" for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"rho <= 0.4\" first_failing_seed={seeds[rho_values.index(min(rho_values))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported_conjecture")