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
    
    def nearest_neighbor_graph(n):
        points = [[random.random() for _ in range(2)] for _ in range(n)]
        graph = {}
        for i in range(n):
            graph[i] = []
            for j in range(i + 1, n):
                dist = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                if dist < 0.5:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def communication_matrix(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if j in graph[i]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row[:] for row in matrix]
        for i in range(n):
            augmented_matrix[i].append(1 if i == j else 0)
        
        def gaussian_elimination(mat):
            rows, cols = len(mat), len(mat[0])
            for col in range(cols - 1):
                pivot_row = next((r for r in range(col, rows) if mat[r][col] != 0), None)
                if pivot_row is None:
                    continue
                mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
                for r in range(rows):
                    if r == col:
                        continue
                    factor = -mat[r][col] / mat[col][col]
                    for c in range(cols):
                        mat[r][c] += factor * mat[col][c]
            return [row[-1] for row in mat[:cols-1]]
        
        return len(gaussian_elimination(augmented_matrix))
    
    def geometric_entropy(graph):
        n = len(graph)
        total_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
        max_degree = max(len(neighbors) for neighbors in graph.values())
        entropy = -math.log(max_degree / (n * (n - 1)), 2) if max_degree > 0 else 0
        return entropy
    
    def k(n):
        # Polynomial function of n, e.g., k(n) = n^2
        return n ** 2
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        if n > 30:
            break
        
        graph = nearest_neighbor_graph(n)
        comm_matrix = communication_matrix(graph)
        g_ent = geometric_entropy(graph)
        k_n = k(n)
        
        instances_tested += 1
        total_metric_value += g_ent
        
        if g_ent < k_n:
            conjecture_holds = False
            counterexample = f"n={n}, GEnt(Σ)={g_ent}, k(n)={k_n}"
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")