# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_planar_graph(n):
        if n == 1:
            return [(0, 1)]
        nodes = list(range(n))
        edges = []
        for i in range(n - 1):
            edges.append((nodes[i], nodes[i + 1]))
        edges.append((nodes[0], nodes[-1]))
        return edges
    
    def lll_reduction(matrix):
        n = len(matrix)
        B = [list(row) for row in matrix]
        d = [Fraction(0, 1)] * n
        u = [Fraction(1, 1)] * n
        beta = [[Fraction(0, 1)] * n for _ in range(n)]
        
        def gram_schmidt():
            for k in range(n):
                B[k] = [B[k][i] - sum(beta[k][j] * B[j][i] for j in range(k)) for i in range(len(B[0]))]
                d[k] = Fraction(sum(B[k][i]**2 for i in range(k + 1)), d[k])
                if k > 0:
                    beta[k][k - 1] = Fraction(u[k], d[k - 1])
        
        def size_reduction():
            for k in range(n):
                for j in range(k - 1, -1, -1):
                    q = B[k][j] // d[j]
                    if abs(q) > 0:
                        B[k] = [B[k][i] - q * B[j][i] for i in range(len(B[0]))]
                        u[k] -= q * u[j]
                        beta[k][j] -= q * beta[j][j]
                if k > 1 and abs(u[k]) >= d[k - 1]:
                    u[k], u[k - 1] = u[k - 1], u[k]
                    B[k], B[k - 1] = B[k - 1], B[k]
                    for j in range(k):
                        beta[k][j], beta[k - 1][j] = beta[k - 1][j], beta[k][j]
        
        gram_schmidt()
        size_reduction()
        
        return [list(row) for row in B]
    
    def minimal_diophantine_degree(graph):
        n = len(graph)
        matrix = [[0] * (n + 2) for _ in range(n + 2)]
        for u, v in graph:
            matrix[u][v] = 1
            matrix[v][u] = 1
            matrix[n][u] += 1
            matrix[n][v] += 1
            matrix[n + 1][n - u] += 1
            matrix[n + 1][n - v] += 1
        
        reduced_matrix = lll_reduction(matrix)
        return sum(abs(reduced_matrix[i][i]) for i in range(n))
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for u, v in graph:
            if matrix[u][v] == 1:
                rank += 1
        return rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = (sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))**0.5
        std_y = (sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))**0.5
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    dd_values = []
    ccr_values = []
    
    for n in n_values:
        graph = generate_planar_graph(n)
        dd_G = minimal_diophantine_degree(graph)
        ccr_G = communication_complexity_rank(graph)
        dd_values.append(dd_G)
        ccr_values.append(ccr_G)
    
    r = correlation_coefficient(dd_values, ccr_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(r),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(r) > 0.8 and r >= 0,
        "counterexample": "" if abs(r) > 0.8 and r >= 0 else f"r={r}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.8 and result["metric_value"] >= 0) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (abs(result["metric_value"]) > 0.8 and result["metric_value"] >= 0))
        print(f"RESULT: FALSIFIED counterexample='r<{mean_r}' first_failing_seed={first_failing_seed}")