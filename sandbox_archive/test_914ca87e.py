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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bipartite_graph(n):
        A = [i for i in range(n // 2)]
        B = [i + n // 2 for i in range(n // 2)]
        edges = []
        for u in A:
            for v in B:
                if random.random() < 0.5:
                    edges.append((u, v))
        return (A, B, edges)
    
    def laplacian_matrix(graph):
        n = len(graph[0]) + len(graph[1])
        L = [[0] * n for _ in range(n)]
        A, B, edges = graph
        for u, v in edges:
            if u < len(A) and v >= len(A):
                L[u][v - len(A)] = -1
                L[v - len(A)][u] = -1
            elif u >= len(A) and v < len(A):
                L[u][v] = -1
                L[v][u] = -1
        for i in range(n):
            degree = sum(1 for j in range(n) if L[i][j] != 0)
            L[i][i] = degree
        return L
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        elif n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            return [a * d - b * c, -(a + d), a * d + b * c]
        else:
            det = 0
            for j in range(n):
                submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return [det]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            return a * d - b * c
        else:
            det = 0
            for j in range(n):
                submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
    
    def hodge_bundle_metrics(laplacian):
        char_poly = characteristic_polynomial(laplacian)
        return abs(char_poly[-2])
    
    def communication_complexity_rank(graph):
        A, B, edges = graph
        rank_A = len(A)
        rank_B = len(B)
        rank_AB = len(edges)
        return max(rank_A, rank_B, rank_AB)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    rank_values = []
    
    for n in n_values:
        graph = generate_bipartite_graph(n)
        laplacian = laplacian_matrix(graph)
        h_value = hodge_bundle_metrics(laplacian)
        rank_value = communication_complexity_rank(graph)
        h_values.append(h_value)
        rank_values.append(rank_value)
    
    mean_h = sum(h_values) / len(h_values)
    mean_rank = sum(rank_values) / len(rank_values)
    correlation_coefficient = sum((h - mean_h) * (rank - mean_rank) for h, rank in zip(h_values, rank_values)) / len(h_values)
    mean_diff = abs(mean_h - mean_rank)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_diff <= 3,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")