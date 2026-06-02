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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def compute_automorphic_representation(graph):
        n = len(graph)
        char_table = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if j in graph[i]:
                    char_table[i][j] = 1
        return char_table

    def min_index(char_table):
        n = len(char_table)
        indices = [sum(row) for row in char_table]
        return max(indices)

    def compute_circuit_width(graph):
        n = len(graph)
        visited = [False] * n
        width = 0
        
        def dfs(u, level):
            nonlocal width
            if visited[u]:
                return
            visited[u] = True
            for v in graph[u]:
                dfs(v, level + 1)
            width = max(width, level)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return width

    n = 40
    d = random.randint(2, n - 2)
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "min_index",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    char_table = compute_automorphic_representation(graph)
    min_index_val = min_index(char_table)
    circuit_width = compute_circuit_width(graph)
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")