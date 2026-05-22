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
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def local_index(graph):
        n = len(graph)
        covered_edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1 and (i, j) not in covered_edges:
                    covered_edges.add((i, j))
                    covered_edges.update([(k, i), (k, j)] for k in range(n) if graph[k][i] == 1 or graph[k][j] == 1)
        return len(covered_edges) // n
    
    def communication_complexity(graph):
        n = len(graph)
        # Simplified version of the disjointness problem communication complexity
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    loc_idx = local_index(graph)
    comm_complexity = communication_complexity(graph)
    
    metric_value = comm_complexity / (loc_idx ** (1/3))
    conjecture_holds = metric_value >= n ** (2/3)
    counterexample = f"n={n}, loc_idx={loc_idx}, comm_complexity={comm_complexity}" if not conjecture_holds else ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")