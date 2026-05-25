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
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        for _ in range(k, n):
            v = random.choice(vertices)
            neighbors = [u for u in vertices if (v, u) in edges or (u, v) in edges]
            new_edges = [(v, u) for u in vertices if u not in neighbors and (v, u) not in edges and (u, v) not in edges]
            if new_edges:
                edge = random.choice(new_edges)
                edges.append(edge)
        return vertices, edges
    
    def incidence_graph_to_quandle_representation(graph):
        n = len(graph[0])
        quandle = [[i for i in range(n)] for _ in range(n)]
        for u, v in graph[1]:
            quandle[u][v] = (quandle[u][v] + 1) % n
            quandle[v][u] = (quandle[v][u] + 1) % n
        return quandle
    
    def min_rank(quandle):
        m, n = len(quandle), len(quandle[0])
        rank = 0
        for i in range(m):
            if any(quandle[i][j] != 0 for j in range(n)):
                pivot_col = next(j for j in range(n) if quandle[i][j] != 0)
                for j in range(i + 1, m):
                    factor = quandle[j][pivot_col] / quandle[i][pivot_col]
                    for k in range(n):
                        quandle[j][k] -= factor * quandle[i][k]
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    k = min(n, 4)  # Ensure at least one edge
    graph = generate_k_clique(n, k)
    if not graph:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    quandle = incidence_graph_to_quandle_representation(graph)
    rank = min_rank(quandle)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= k,
        "counterexample": "" if rank >= k else f"rank={rank}, expected>=k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")