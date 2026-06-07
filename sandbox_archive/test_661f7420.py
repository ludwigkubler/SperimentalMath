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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d // 2)
            for j in neighbors:
                edge = tuple(sorted((i, j)))
                if edge not in edges and (j, i) not in edges:
                    edges.add(edge)
        return list(edges)
    
    def get_automorphism_group(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def is_permutation(p):
            return all(p[i] == i for i in range(n))
        
        def apply_permutation(p, g):
            new_g = []
            for u, v in g:
                new_g.append((p[u], p[v]))
            return new_g
        
        automorphisms = [list(range(n))]
        visited = set()
        stack = [list(range(n))]
        
        while stack:
            p = stack.pop()
            if is_permutation(p):
                for u, v in graph:
                    new_p = [p[i] for i in range(n)]
                    new_p[u], new_p[v] = new_p[v], new_p[u]
                    new_g = apply_permutation(new_p, graph)
                    if tuple(sorted(new_g)) not in visited:
                        automorphisms.append(new_p)
                        visited.add(tuple(sorted(new_g)))
                        stack.append(new_p)
        
        return automorphisms
    
    def get_symmetry_breaking_number(automorphisms):
        return len(automorphisms) - 1
    
    def get_communication_complexity_rank(graph):
        n = len(graph)
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def dfs(v, visited, path):
            if len(path) > 1 and path[-2] == v:
                return
            visited.add(v)
            path.append(v)
            for u in range(n):
                if adj_matrix[v][u] == 1 and u not in visited:
                    dfs(u, visited, path)
            path.pop()
            visited.remove(v)
        
        def get_geodesics(graph):
            geodesics = []
            for v in range(n):
                visited = set()
                path = []
                dfs(v, visited, path)
                geodesics.extend(path)
            return geodesics
        
        geodesics = get_geodesics(graph)
        unique_geodesics = list(set(tuple(sorted(g)) for g in geodesics))
        return len(unique_geodes)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * (n - 1) % (d * 2) != 0:
            continue
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        
        automorphisms = get_automorphism_group(graph)
        sbn = get_symmetry_breaking_number(automorphisms)
        r = get_communication_complexity_rank(graph)
        
        results.append((sbn, r))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(results)
    x_sum = sum(x for x, _ in results)
    y_sum = sum(y for _, y in results)
    xy_sum = sum(x * y for x, y in results)
    x2_sum = sum(x ** 2 for x, _ in results)
    y2_sum = sum(y ** 2 for _, y in results)
    
    x_mean = Fraction(x_sum, n)
    y_mean = Fraction(y_sum, n)
    
    numerator = xy_sum * n - x_sum * y_sum
    denominator = math.sqrt((x2_sum * n - x_sum ** 2) * (y2_sum * n - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = Fraction(numerator, denominator)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(pearson_corr),
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(float(pearson_corr)) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")