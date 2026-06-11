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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def term_graph(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                if literal not in graph:
                    graph[literal] = set()
                for other_literal in clause:
                    if other_literal != literal and -literal not in clause:
                        graph[literal].add(other_literal)
        return graph

    def min_group_order(graph):
        n = len(graph)
        order = 0
        visited = [False] * (2 * n + 1)
        
        def dfs(node, current_order):
            if visited[node]:
                return current_order
            visited[node] = True
            for neighbor in graph.get(node, set()):
                current_order = max(current_order, dfs(neighbor, current_order))
            return current_order
        
        for node in range(-n, n + 1):
            if not visited[node]:
                order += dfs(node, 0)
        
        return order

    def communication_complexity_rank_variance(cnf):
        rank_variances = []
        for _ in range(10):  # Sample multiple times to get a good estimate
            assignment = {i: random.choice([True, False]) for i in range(1, n + 1)}
            rank = sum(1 for clause in cnf if any(literal in assignment and (literal > 0) == assignment[literal] for literal in clause))
            rank_variances.append(rank)
        return math.variance(rank_variances)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        graph = term_graph(cnf)
        order = min_group_order(graph)
        rank_variance = communication_complexity_rank_variance(cnf)
        results.append((order, rank_variance))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    orders = [r[0] for r in results]
    rank_variances = [r[1] for r in results]
    correlation = sum((orders[i] - mean(orders)) * (rank_variances[i] - mean(rank_variances)) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")