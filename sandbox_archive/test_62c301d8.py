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
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def matroid_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    u = stack.pop()
                    if not visited[u]:
                        visited[u] = True
                        rank += 1
                        for v in graph[u]:
                            if not visited[v]:
                                stack.append(v)
        return rank
    
    def geometric_entropy(matroid_rank):
        n = matroid_rank
        if n == 0:
            return 0
        entropy = -n * math.log2(n) / (n * (n - 1))
        return entropy
    
    def tseitin_formula(graph):
        n = len(graph)
        num_vars = 2 * n + 1
        clauses = []
        for i in range(n):
            clauses.append([i + 1, -(n + i + 1)])
            for j in graph[i]:
                if j > i:
                    clauses.append([-i - 1, -j - 1, j + 1])
        return num_vars, clauses
    
    def resolution_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_max = 40
    instances_tested = 0
    mge_values = []
    w_values = []
    
    for _ in range(30):
        d = random.randint(2, min(n_max - 1, 5 * (n_max // 10)))
        graph = generate_d_regular_graph(n_max, d)
        if graph is None:
            continue
        matroid_rank_val = matroid_rank(graph)
        mge_value = geometric_entropy(matroid_rank_val)
        num_vars, clauses = tseitin_formula(graph)
        w_value = resolution_width(clauses)
        
        if mge_value > 10 or w_value < 3:
            continue
        
        instances_tested += 1
        mge_values.append(mge_value)
        w_values.append(w_value)
    
    if instances_tested == 0:
        return {
            "metric_name": "mge(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((x - m) * (y - n) for x, y in zip(mge_values, w_values)) / math.sqrt(sum((x - m) ** 2 for x in mge_values) * sum((y - n) ** 2 for y in w_values))
    
    return {
        "metric_name": "mge(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for result in results if result["conjecture_holds"])
    
    if support_count >= 25:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_count/len(results)}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")