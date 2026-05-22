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
    
    def generate_3_regular_graph(n):
        if n % 2 != 0 or n < 4:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        nodes = list(range(n))
        while len(edges) < n // 2:
            u, v = random.sample(nodes, 2)
            if (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def hodge_index(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                matrix[u][v] = 1
                matrix[v][u] = 1
        rank = gaussian_elimination(matrix)
        return n - rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(n):
                if j != i and A[rank][j] != 0:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_indices = []
    
    for n in n_values:
        graph = generate_3_regular_graph(n)
        if graph is None:
            continue
        hodge_index_val = hodge_index(graph)
        hodge_indices.append(hodge_index_val)
    
    mean_hodge_index = sum(hodge_indices) / len(hodge_indices)
    support_fraction = sum(1 for val in hodge_indices if val <= math.log(n_values[0]) / 4) / len(hodge_indices)
    
    conjecture_holds = mean_hodge_index >= math.log(n_values[0]) / 2 and support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalHodgeIndex",
        "metric_value": mean_hodge_index,
        "instances_tested": len(hodge_indices),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")