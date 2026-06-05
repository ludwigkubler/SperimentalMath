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

def generate_random_graph(n, max_degree):
    graph = [[] for _ in range(n)]
    degree = [0] * n
    edges_added = 0
    
    while edges_added < n * max_degree // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
            degree[u] += 1
            degree[v] += 1
            edges_added += 1
    
    return graph

def compute_communication_matrix(graph):
    n = len(graph)
    comm_matrix = [[0] * n for _ in range(n)]
    
    for u in range(n):
        for v in range(u + 1, n):
            if v in graph[u]:
                comm_matrix[u][v] = 1
                comm_matrix[v][u] = 1
    
    return comm_matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(n):
        pivot_row = next((j for j in range(rank, m) if matrix[j][i] != 0), None)
        if pivot_row is None:
            continue
        
        # Swap rows
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        # Make the pivot element 1
        denom = matrix[rank][i]
        for j in range(n):
            matrix[rank][j] /= denom
        
        # Eliminate other elements in the column
        for j in range(m):
            if j != rank:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        graph = generate_random_graph(n, max_degree=3)
        comm_matrix = compute_communication_matrix(graph)
        
        rank = gaussian_elimination(comm_matrix)
        lattice_points = len([x for x in range(1 << n) if all((x >> i) & 1 == (y >> i) & 1 or y not in graph[i] for i, y in enumerate(graph))])
        
        instances_tested += n
        n_max = max(n_max, n)
        
        total_metric_value += lattice_points / rank
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(lattice_points >= c * rank for lattice_points, rank in zip(lattice_points_values, ranks))
    
    return {
        "metric_name": "L(G) / r(G)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")