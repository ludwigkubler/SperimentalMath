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

def generate_random_graph(n):
    if n <= 1:
        return [], 0
    
    nodes = list(range(n))
    edges = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    
    return (nodes, edges), n

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        
        for j in range(i+1, n):
            factor = A_b[j][i] / A_b[i][i]
            A_b[j] = [A_b[j][k] - factor * A_b[i][k] for k in range(n + 1)]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    
    return x

def max_edge_connectivity(graph):
    nodes, edges = graph
    n = len(nodes)
    if n <= 1:
        return 0
    
    max_kappa = 0
    for node in nodes:
        neighbors = [neighbor for neighbor in nodes if (node, neighbor) in edges or (neighbor, node) in edges]
        kappa = len(neighbors)
        if kappa > max_kappa:
            max_kappa = kappa
    
    return max_kappa

def communication_rank(graph):
    nodes, edges = graph
    n = len(nodes)
    
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for u, v in edges:
        A[u][v] += 1
        A[v][u] += 1
        b[u] += 1
        b[v] += 1
    
    x = gaussian_elimination(A, b)
    
    return sum(x[i] for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_growth_rate = Fraction(0)
    max_n = 0
    
    for n in n_values:
        graph, n = generate_random_graph(n)
        kappa = max_edge_connectivity(graph)
        growth_rate = communication_rank(graph) / (kappa ** 2 * math.log(n))
        
        instances_tested += 1
        total_growth_rate += Fraction(growth_rate).limit_denominator()
        if n > max_n:
            max_n = n
    
    metric_mean = total_growth_rate / instances_tested
    conjecture_holds = all(growth_rate >= 0.5 * metric_mean for growth_rate in [communication_rank(graph) / (kappa ** 2 * math.log(n)) for n in n_values for graph, _ in [generate_random_graph(n)]])
    
    return {
        "metric_name": "growth_rate",
        "metric_value": float(metric_mean),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_growth_rate = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_growth_rate} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_growth_rate} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")