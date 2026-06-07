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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def projective_plane_points(graph):
        n = len(graph)
        points = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in graph:
                    point = (i, j)
                    points.add(point)
        return len(points)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if j not in neighbors:
                    common_neighbors = set(graph[j]) & neighbors
                    rank += len(common_neighbors)
        return rank
    
    def run_test(n, d):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            return {"metric_name": "points_to_rank_ratio", "metric_value": float('inf'), "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "graph_not_possible"}
        
        points = projective_plane_points(graph)
        rank = communication_complexity_rank(graph)
        ratio = points / rank if rank != 0 else float('inf')
        return {"metric_name": "points_to_rank_ratio", "metric_value": ratio, "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}
    
    results = []
    for d in [2, 3, 4]:
        for _ in range(10):
            result = run_test(random.randint(5, 40), d)
            results.append(result)
    
    total_points = sum(r["metric_value"] * r["instances_tested"] for r in results)
    total_rank = sum(r["instances_tested"] for r in results)
    mean_ratio = total_points / total_rank if total_rank != 0 else float('inf')
    
    conjecture_holds = all(0.5 <= r["metric_value"] <= 1.5 for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    
    return {"metric_name": "points_to_rank_ratio", "metric_value": mean_ratio, "instances_tested": len(results), "n_max": 40, "conjecture_holds": conjecture_holds, "counterexample": counterexample}

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 1.5) / len(results)
    
    if all(0.5 <= r["metric_value"] <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")