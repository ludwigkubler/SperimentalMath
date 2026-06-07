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
    
    def generate_d_regular_graph(n: int, d: int):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph

    def projective_plane_points(graph):
        points = set()
        for node in graph:
            for neighbor in graph[node]:
                points.add((node, neighbor))
        return len(points)

    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        queue = [0]
        while queue:
            u = queue.pop()
            if not visited[u]:
                visited[u] = True
                for v in graph[u]:
                    if not visited[v]:
                        queue.append(v)
                        rank += 1
        return rank

    d = 3
    results = []
    for n in range(10, 41):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        points = projective_plane_points(graph)
        rank = communication_complexity_rank(graph)
        if rank == 0:
            continue
        results.append((points, rank))

    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    ratios = [points / rank for points, rank in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    conjecture_holds = all(0.5 <= ratio <= 1.5 for ratio in ratios)
    counterexample = "" if conjecture_holds else "ratio_out_of_bounds"

    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
        support_fraction = sum("conjecture_holds" in result and result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")