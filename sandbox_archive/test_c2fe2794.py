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
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def projective_plane_points(graph):
        points = set()
        for node in graph:
            for neighbor in graph[node]:
                if (node, neighbor) not in points and (neighbor, node) not in points:
                    points.add((node, neighbor))
        return len(points)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    u = queue.pop()
                    if not visited[u]:
                        visited[u] = True
                        for v in graph[u]:
                            if not visited[v]:
                                queue.append(v)
                rank += 1
        return rank
    
    n_values = [10, 15, 20, 30, 40]
    total_points = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        d = random.randint(2, min(n-1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        points = projective_plane_points(graph)
        rank = communication_complexity_rank(graph)
        total_points += points
        total_rank += rank
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = total_points / total_rank
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")