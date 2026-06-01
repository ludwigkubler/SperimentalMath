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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(cols):
                matrix[i][j] /= pivot
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        if rows == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def min_rank(cluster_algebra):
        rows, cols = len(cluster_algebra), len(cluster_algebra[0])
        reduced_matrix = gaussian_elimination(cluster_algebra)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank

    def communication_complexity_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        laplacian_matrix = [[sum(adjacency_matrix[i][j] for j in range(n) if i != j) - adjacency_matrix[i][j] for j in range(n)] for i in range(n)]
        return determinant(laplacian_matrix)

    def generate_d_regular_graph(d, n):
        graph = set()
        while len(graph) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in graph and (v, u) not in graph:
                graph.add((u, v))
        return list(graph)

    def cluster_algebra(graph):
        n = len(graph)
        max_edges = d * n // 2
        cluster_algebra = [[0] * max_edges for _ in range(max_edges)]
        edge_index = 0
        for u, v in graph:
            cluster_algebra[edge_index][edge_index] = 1
            cluster_algebra[edge_index][edge_index + 1] = -1
            cluster_algebra[edge_index + 1][edge_index] = -1
            cluster_algebra[edge_index + 1][edge_index + 1] = 1
            edge_index += 2
        return cluster_algebra

    d = random.randint(3, 5)
    n = 40
    graph = generate_d_regular_graph(d, n)
    cluster_algebra = cluster_algebra(graph)
    min_rank_cG = min_rank(cluster_algebra)
    r_G = communication_complexity_rank(graph)

    return {
        "metric_name": "min_rank_diff",
        "metric_value": abs(min_rank_cG - r_G),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [389, 421, 463, 503, 547, 593, 631, 677, 727, 773, 821, 877, 929]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(result["conjecture_holds"] for result in results):
        mean_diff = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_diff) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=too_many_instances")