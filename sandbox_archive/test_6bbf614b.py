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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u == v or (u, v) in edges_added or (v, u) in edges_added:
            continue
        
        graph[u].append(v)
        graph[v].append(u)
        edges_added.add((u, v))
    
    return graph

def compute_mcl(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            adjacency_matrix[u][v] = 1
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(m):
            if matrix[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    mcl = gaussian_elimination(adjacency_matrix)
    
    return mcl

def compute_rank_variance(graph):
    n = len(graph)
    if n == 0:
        return 0
    
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            adjacency_matrix[u][v] = 1
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(m):
            if matrix[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    rank = gaussian_elimination(adjacency_matrix)
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(2, 4)
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        mcl = compute_mcl(graph)
        rank_variance = compute_rank_variance(graph)
        
        if math.isinf(mcl) or math.isnan(mcl):
            continue
        
        instances_tested += 1
        metric_values.append((mcl, rank_variance))
    
    if instances_tested == 0:
        return {
            "metric_name": "mcl(G)",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Failed to generate a valid d-regular graph"
        }
    
    msl = [x[0] for x in metric_values]
    rsv = [x[1] for x in metric_values]
    
    mean_mcl = sum(msl) / instances_tested
    mean_rsv = sum(rsv) / instances_tested
    
    covariance = sum((msl[i] - mean_mcl) * (rsv[i] - mean_rsv) for i in range(instances_tested)) / instances_tested
    variance_mcl = sum((msl[i] - mean_mcl) ** 2 for i in range(instances_tested)) / instances_tested
    variance_rsv = sum((rsv[i] - mean_rsv) ** 2 for i in range(instances_tested)) / instances_tested
    
    correlation_coefficient = covariance / (math.sqrt(variance_mcl) * math.sqrt(variance_rsv))
    
    return {
        "metric_name": "mcl(G)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if not math.isnan(x["metric_value"])) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results if not math.isnan(x["metric_value"])) / len(results))
    
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(math.isnan(x["metric_value"]) for x in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")