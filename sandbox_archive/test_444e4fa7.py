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
    
    def generate_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def laplacian_matrix(graph, n):
        L = [[0] * n for _ in range(n)]
        degree = [0] * n
        for u, v in graph:
            L[u][v] = 1
            L[v][u] = 1
            degree[u] += 1
            degree[v] += 1
        for i in range(n):
            L[i][i] = -degree[i]
        return L
    
    def tropicalize(matrix):
        n = len(matrix)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if matrix[i][j] >= 0:
                    T[i][j] = matrix[i][j]
        return T
    
    def rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        pivot_row = 0
        for i in range(n):
            if A[pivot_row][i] == 0:
                continue
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[j], A[pivot_row] = A[pivot_row], A[j]
                    break
            else:
                continue
            for j in range(n):
                if j == i:
                    continue
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
            pivot_row += 1
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    L_G = laplacian_matrix(graph, n)
    T_L_G = tropicalize(L_G)
    rho_L_G = rank(T_L_G)
    
    K_n_n_edges = [(i, i + n) for i in range(n)] + [(i + n, i) for i in range(n)]
    L_IP_2 = laplacian_matrix(K_n_n_edges, 2 * n)
    T_L_IP_2 = tropicalize(L_IP_2)
    rho_L_IP_2 = rank(T_L_IP_2)
    
    metric_name = "rho"
    metric_value = (rho_L_G, rho_L_IP_2)
    instances_tested = 1
    conjecture_holds = rho_L_G <= math.log(n) and rho_L_IP_2 >= n**2
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"][0] - mean_metric_value)**2 + (result["metric_value"][1] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {results[seeds.index(first_failing_seed)]['metric_value'][0]} vertices\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")