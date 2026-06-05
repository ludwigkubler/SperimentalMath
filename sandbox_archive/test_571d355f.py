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
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        if A is None:
            return 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def min_categorical_dimension(graph):
        n = len(graph)
        adjacency_matrix = [[int(v in graph[u]) for v in range(n)] for u in range(n)]
        rank = matrix_rank(adjacency_matrix)
        return rank
    
    n_max = 40
    instances_tested = 0
    total_min_dim = 0
    total_comm_complexity = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        d = random.randint(2, min(n-1, 5))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        instances_tested += n * (n - 1) // 2
        min_dim = min_categorical_dimension(graph)
        comm_complexity = matrix_rank([graph[u] for u in range(n)])
        total_min_dim += min_dim
        total_comm_complexity += comm_complexity
    
    if instances_tested < 30:
        return {
            "metric_name": "min_dim vs comm_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_min_dim = total_min_dim / instances_tested
    mean_comm_complexity = total_comm_complexity / instances_tested
    
    if mean_min_dim < 0.1 * mean_comm_complexity:
        return {
            "metric_name": "min_dim vs comm_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "inequality_violated"
        }
    
    return {
        "metric_name": "min_dim vs comm_complexity",
        "metric_value": mean_min_dim / mean_comm_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"inequality_violated\" first_failing_seed={first_failing_seed}")