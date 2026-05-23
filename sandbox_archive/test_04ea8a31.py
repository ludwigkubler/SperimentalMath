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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        det = 1
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            if i != max_row:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                det *= -1
            det *= matrix[i][i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return det

    def minimal_representation_rank(G):
        n = len(G)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [[0 for _ in range(n)] for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        A_inv = gaussian_elimination(A)
        det_A_inv = determinant(A_inv)
        return int(math.log2(abs(det_A_inv)))

    def tseitin_formula_resolution_depth(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append((i,))
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return len(clauses)

    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append((i,))
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return random.choice(clauses)

    def covering_graph(G):
        n = len(G)
        graph = [[] for _ in range(n)]
        for u, v in G:
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)

    def generate_groupoid(n):
        G = []
        for i in range(n):
            for j in range(i + 1, n):
                G.append((i, j))
        return G

    def minimal_representation_rank(G):
        n = len(G)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [[0 for _ in range(n)] for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        A_inv = gaussian_elimination(A)
        det_A_inv = determinant(A_inv)
        return int(math.log2(abs(det_A_inv)))

    def tseitin_formula_resolution_depth(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append((i,))
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return len(clauses)

    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append((i,))
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append((-i, -j))
                clauses.append((i, j))
        return random.choice(clauses)

    def covering_graph(G):
        n = len(G)
        graph = [[] for _ in range(n)]
        for u, v in G:
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)

    def generate_groupoid(n):
        G = []
        for i in range(n):
            for j in range(i + 1, n):
                G.append((i, j))
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_tseitin_formula(n)
            depth = tseitin_formula_resolution_depth(n)
            G = generate_groupoid(n)
            rank = minimal_representation_rank(G)
            results.append({"depth": depth, "rank": rank})

    mean_depth = sum(result["depth"] for result in results) / len(results)
    std_depth = math.sqrt(sum((result["depth"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["rank"] >= 2 ** result["depth"]) / len(results)

    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else "support_fraction < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_depth = sum(result["metric_value"] for result in results) / len(results)
    std_depth = math.sqrt(sum((result["metric_value"] - mean_depth) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.8' first_failing_seed={first_failing_seed}")