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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0 or k < 1 or k >= n:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * k // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, cols):
                matrix[i][j] /= matrix[i][i]
            matrix[i][i] = 1
            for j in range(rows):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        if reduced_matrix is None:
            return float('inf')
        rank = 0
        for row in reduced_matrix:
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity_rank(graph, subgraph):
        n = len(graph)
        subgraph_matrix = [[graph[i][j] for j in range(n) if subgraph[j]] for i in range(n)]
        return rank(subgraph_matrix)
    
    def minimal_local_index(graph):
        n = len(graph)
        total_edges = sum(sum(row) for row in graph) // 2
        return total_edges / (n * (n - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_k_regular_graph(n, k=3)
        if graph is None:
            continue
        mli = minimal_local_index(graph)
        subgraph_ranks = [communication_complexity_rank(graph, [i]) for i in range(n)]
        variance = sum((x - sum(subgraph_ranks) / len(subgraph_ranks)) ** 2 for x in subgraph_ranks) / len(subgraph_ranks)
        results.append({"n": n, "mli": mli, "variance": variance})
    
    if not results:
        return {
            "metric_name": "minimal_local_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mli_values = [result["mli"] for result in results]
    variance_values = [result["variance"] for result in results]
    if any(v == 0 for v in variance_values):
        return {
            "metric_name": "minimal_local_index",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    ratio = min(mli_values) / max(variance_values)
    return {
        "metric_name": "minimal_local_index",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": ratio >= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")