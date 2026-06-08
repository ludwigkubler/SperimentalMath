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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for v in range(n):
            neighbors = random.sample(range(v + 1, n), d - len(graph[v]))
            for u in neighbors:
                if (v, u) not in edges_used and (u, v) not in edges_used:
                    graph[v].append(u)
                    graph[u].append(v)
                    edges_used.add((v, u))
        return graph
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([-i, -j])
                clauses.append([-i, j])
                clauses.append([i, -j])
        return clauses
    
    def resolution_width(clauses):
        queue = set()
        learned_clauses = []
        while True:
            new_clause = None
            for clause in queue:
                if len(clause) == 1:
                    literal = clause[0]
                    for other_clause in queue:
                        if -literal in other_clause:
                            new_clause = [l for l in other_clause if l != -literal]
                            break
                    if new_clause is not None:
                        break
            if new_clause is None:
                return len(learned_clauses)
            learned_clauses.append(new_clause)
            queue.update([c.union(new_clause) for c in queue])
            queue.add(frozenset(new_clause))
    
    def min_order(graph):
        n = len(graph)
        orders = [0] * n
        visited = [False] * n
        
        def dfs(v, order):
            if not visited[v]:
                visited[v] = True
                for u in graph[v]:
                    dfs(u, order + 1)
                orders[v] = order
        
        for v in range(n):
            dfs(v, 0)
        
        return math.lcm(*orders)
    
    def generate_random_d_regular_graphs(n, d, num_graphs=30):
        graphs = []
        for _ in range(num_graphs):
            graph = generate_d_regular_graph(n, d)
            if graph is not None:
                graphs.append(graph)
        return graphs
    
    n = 15
    d = 2
    graphs = generate_random_d_regular_graphs(n, d)
    
    if len(graphs) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(graphs),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_graphs"
        }
    
    min_orders = [min_order(graph) for graph in graphs]
    tseitin_clauses = [tseitin_formula(n) for _ in range(len(graphs))]
    widths = [resolution_width(clause) for clause in tseitin_clauses]
    
    correlation_coefficient = 0
    n_tested = len(min_orders)
    if n_tested > 1:
        mean_min_order = sum(min_orders) / n_tested
        mean_width = sum(widths) / n_tested
        numerator = sum((min_orders[i] - mean_min_order) * (widths[i] - mean_width) for i in range(n_tested))
        denominator = math.sqrt(sum((min_orders[i] - mean_min_order) ** 2 for i in range(n_tested))) * math.sqrt(sum((widths[i] - mean_width) ** 2 for i in range(n_tested)))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tested,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")