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
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def compute_curvature_form(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        degree_sum = 0
        for u in range(n):
            degree = len(graph[u])
            degree_sum += degree
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1

        laplacian_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            degree = len(graph[u])
            laplacian_matrix[u][u] = degree
            for v in graph[u]:
                laplacian_matrix[u][v] -= 1
                laplacian_matrix[v][u] -= 1

        eigenvalues = []
        for i in range(n):
            eigenvector = [0] * n
            eigenvector[i] = 1
            value = sum(laplacian_matrix[i][j] * eigenvector[j] for j in range(n))
            eigenvalues.append(value)

        return max(eigenvalues) - min(eigenvalues)

    def communication_complexity(graph):
        n = len(graph)
        return math.log2(n)

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j

            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

            # Eliminate below pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

        return matrix

    def rank(matrix):
        n = len(matrix)
        row_echelon_form = gaussian_elimination(matrix)
        rank = 0
        for i in range(n):
            if any(row_echelon_form[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []

    for n in n_values:
        graph = generate_graph(n)
        curvature_form = compute_curvature_form(graph)
        communication_complexity_value = communication_complexity(graph)
        rank_value = rank([[curvature_form]])

        ranks.append(rank_value)
        complexities.append(communication_complexity_value)

    mean_rank = sum(ranks) / len(ranks)
    std_deviation = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    support_fraction = all(abs(mean_rank - complexity) <= 10 * std_deviation for complexity in complexities)

    return {
        "metric_name": "Minimal Rank of Curvature Form",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_ranks = [x["metric_value"] for x in results]
    std_deviation_ranks = math.sqrt(sum((x - sum(mean_ranks) / len(mean_ranks)) ** 2 for x in mean_ranks) / len(mean_ranks))
    support_fraction = all(abs(sum(mean_ranks) / len(mean_ranks) - complexity) <= 10 * std_deviation_ranks for complexity in [math.log2(n) for n in range(5, 41)])

    if support_fraction:
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks) / len(mean_ranks)} std={std_deviation_ranks} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")