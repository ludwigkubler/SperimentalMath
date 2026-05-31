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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_added:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_added.add((i, j))
        return graph
    
    def automorphism_group_size(graph):
        n = len(graph)
        visited = [False] * n
        group_size = 1
        
        def dfs(node, perm):
            if visited[node]:
                return True
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    new_perm = perm[:]
                    new_perm[neighbor] = perm[node]
                    if not dfs(neighbor, new_perm):
                        return False
            return True
        
        def find_fixed_points(perm):
            fixed_points = []
            for i in range(n):
                if perm[i] == i:
                    fixed_points.append(i)
            return fixed_points
        
        def generate_permutations(fixed_points):
            n_fixed = len(fixed_points)
            if n_fixed == 0:
                yield {}
                return
            for p in itertools.permutations(range(n_fixed)):
                perm = {fixed_points[i]: fixed_points[p[i]] for i in range(n_fixed)}
                yield perm
        
        def is_valid_permutation(perm):
            for node in range(n):
                if perm[node] != node:
                    continue
                new_graph = {i: [j for j in graph[i] if j not in perm.values()] for i in range(n)}
                if not dfs(node, perm):
                    return False
            return True
        
        fixed_points = find_fixed_points({})
        for perm in generate_permutations(fixed_points):
            if is_valid_permutation(perm):
                group_size *= len(perm)
        
        return group_size
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clause = [f"X{i}"]
            for j in graph[i]:
                clause.append(f"-X{j}")
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i]:
                    clause = [f"-X{i}", f"-X{j}", f"X{2 * n + i}"]
                    clauses.append(clause)
                    clause = [f"-X{i}", f"-X{j}", f"X{2 * n + j}"]
                    clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i]:
                    clause = [f"-X{2 * n + i}", f"-X{2 * n + j}", f"X{i}"]
                    clauses.append(clause)
                    clause = [f"-X{2 * n + i}", f"-X{2 * n + j}", f"X{j}"]
                    clauses.append(clause)
        return clauses
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    d_values = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    for d in d_values:
        for _ in range(30):
            n = random.randint(5, 40)
            graph = generate_d_regular_graph(d, n)
            if graph is None:
                continue
            group_size = automorphism_group_size(graph)
            formula = tseitin_formula(graph)
            results.append((math.log(group_size), len(formula)))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*results)
    correlation = pearson_correlation(x, y)
    mean_C = sum(math.log(group_size) / len(formula) for group_size, formula in results) / len(results)
    support_fraction = sum(1 for _, _ in results if 0.5 <= math.log(group_size) / len(formula) <= 1.5) / len(results)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(len(formula) for _, formula in results),
        "conjecture_holds": correlation >= 0.8 and support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    correlation_values = [r["metric_value"] for r in results if "metric_value" in r and not math.isnan(r["metric_value"])]
    support_fractions = [r["conjecture_holds"] for r in results]
    
    mean_corr = sum(correlation_values) / len(correlation_values)
    std_corr = math.sqrt(sum((x - mean_corr) ** 2 for x in correlation_values) / len(correlation_values))
    support_fraction = sum(support_fractions) / len(support_fractions)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")