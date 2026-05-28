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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def resistance_distance(graph, v1, v2):
        n = len(graph)
        dist = [math.inf] * n
        dist[v1] = 0
        queue = [v1]
        
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if (u, v) in graph or (v, u) in graph:
                    new_dist = dist[u] + 1 / len(graph)
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        queue.append(v)
        
        return dist[v2]
    
    def minimal_rank(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for u, v in graph:
            A[u][v], A[v][u] = 1, 1
        
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                for j in range(i + 1, n):
                    if any(A[k][j] != 0 for k in range(i)):
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
                rank += 1
                for j in range(n):
                    A[j][i] /= A[i][i]
                for j in range(n):
                    if j != i:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
        
        return rank
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    v1, v2 = random.sample(range(n), 2)
    
    min_rank = minimal_rank(graph)
    res_dist = resistance_distance(graph, v1, v2)
    
    return {
        "metric_name": "minimal rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": f"Graph with n={n}, minimal rank={min_rank}, resistance distance={res_dist}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")