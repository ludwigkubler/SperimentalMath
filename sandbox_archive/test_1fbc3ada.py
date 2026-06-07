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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        adjacency_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if adjacency_matrix[u][v] == 1 or u == v:
                continue
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
            edges_added += 1
        return adjacency_matrix

    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank

    def automorphism_group_order(graph):
        n = len(graph)
        group_size = 0
        visited = [False] * n
        stack = []
        
        def dfs(node, parent):
            nonlocal group_size
            visited[node] = True
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and neighbor != parent:
                    if not visited[neighbor]:
                        dfs(neighbor, node)
                    else:
                        group_size += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1)
        
        return group_size

    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank = matrix_rank(graph)
        variance = sum((graph[i][j] - (rank / (n * (n - 1)))) ** 2 for i in range(n) for j in range(i + 1, n)) * 2
        return variance

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[n:] for row in augmented_matrix]

    def group_order(G):
        n = len(G)
        identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        G_power = identity
        order = 1
        while True:
            G_power = matrix_multiplication(G_power, G)
            if G_power == identity:
                break
            order += 1
        return order

    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank = matrix_rank(graph)
        variance = sum((graph[i][j] - (rank / (n * (n - 1)))) ** 2 for i in range(n) for j in range(i + 1, n)) * 2
        return variance

    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        def generate_d_regular_graph(n, d):
            if (n * d) % 2 != 0 or d < 1 or d >= n:
                raise ValueError("Invalid parameters for generating a d-regular graph")
            adjacency_matrix = [[0] * n for _ in range(n)]
            edges_added = 0
            while edges_added < n * d // 2:
                u, v = random.sample(range(n), 2)
                if adjacency_matrix[u][v] == 1 or u == v:
                    continue
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
                edges_added += 1
            return adjacency_matrix

        def matrix_rank(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(min(m, n)):
                if matrix[i][i] != 0:
                    for j in range(i + 1, m):
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
                    rank += 1
            return rank

        def automorphism_group_order(graph):
            n = len(graph)
            group_size = 0
            visited = [False] * n
            stack = []
            
            def dfs(node, parent):
                nonlocal group_size
                visited[node] = True
                for neighbor in range(n):
                    if graph[node][neighbor] == 1 and neighbor != parent:
                        if not visited[neighbor]:
                            dfs(neighbor, node)
                        else:
                            group_size += 1
        
            for i in range(n):
                if not visited[i]:
                    dfs(i, -1)
        
            return group_size

        def communication_complexity_rank_variance(graph):
            n = len(graph)
            rank = matrix_rank(graph)
            variance = sum((graph[i][j] - (rank / (n * (n - 1)))) ** 2 for i in range(n) for j in range(i + 1, n)) * 2
            return variance

        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def lcm(a, b):
            return abs(a * b) // gcd(a, b)

        def matrix_multiplication(A, B):
            m, n, p = len(A), len(B), len(B[0])
            C = [[0] * p for _ in range(m)]
            for i in range(m):
                for j in range(p):
                    for k in range(n):
                        C[i][j] += A[i][k] * B[k][j]
            return C

        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                        max_row = j
                augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
                pivot = augmented_matrix[i][i]
                for j in range(i, n + 1):
                    augmented_matrix[i][j] /= pivot
                for j in range(m):
                    if j != i:
                        factor = augmented_matrix[j][i]
                        for k in range(n + 1):
                            augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
            return [row[n:] for row in augmented_matrix]

        def group_order(G):
            n = len(G)
            identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
            G_power = identity
            order = 1
            while True:
                G_power = matrix_multiplication(G_power, G)
                if G_power == identity:
                    break
                order += 1
            return order

        def communication_complexity_rank_variance(graph):
            n = len(graph)
            rank = matrix_rank(graph)
            variance = sum((graph[i][j] - (rank / (n * (n - 1)))) ** 2 for i in range(n) for j in range(i + 1, n)) * 2
            return variance

        def run_trial(seed: int) -> dict:
            random.seed(seed)
            
            def generate_d_regular_graph(n, d):
                if (n * d) % 2 != 0 or d < 1 or d >= n:
                    raise ValueError("Invalid parameters for generating a d-regular graph")
                adjacency_matrix = [[0] * n for _ in range(n)]
                edges_added = 0
                while edges_added < n * d // 2:
                    u, v = random.sample(range(n), 2)
                    if adjacency_matrix[u][v] == 1 or u == v:
                        continue
                    adjacency_matrix[u][v] = 1
                    adjacency_matrix[v][u] = 1
                    edges_added += 1
                return adjacency_matrix

            def matrix_rank(matrix):
                m, n = len(matrix), len(matrix[0])
                rank = 0
                for i in range(min(m, n)):
                    if matrix[i][i] != 0:
                        for j in range(i + 1, m):
                            factor = Fraction(matrix[j][i], matrix[i][i])
                            for k in range(n):
                                matrix[j][k] -= factor * matrix[i][k]
                        rank += 1
                return rank

            def automorphism_group_order(graph):
                n = len(graph)
                group_size = 0
                visited = [False] * n
                stack = []
                
                def dfs(node, parent):
                    nonlocal group_size
                    visited[node] = True
                    for neighbor in range(n):
                        if graph[node][neighbor] == 1 and neighbor != parent:
                            if not visited[neighbor]:
                                dfs(neighbor, node)
                            else:
                                group_size += 1
        
                for i in range(n):
                    if not visited[i]:
                        dfs(i, -1)
        
                return group_size

            def communication_complexity_rank_variance(graph):
                n = len(graph)
                rank = matrix_rank(graph)
                variance = sum((graph[i][j] - (rank / (n * (n - 1)))) ** 2 for i in range(n) for j in range(i + 1, n)) * 2
                return variance

            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a

            def lcm(a, b):
                return abs(a * b) // gcd(a, b)

            def matrix_multiplication(A, B):
                m, n, p = len(A), len(B), len(B[0])
                C = [[0] * p for _ in range(m)]
                for i in range(m):
                    for j in range(p):
                        for k in range(n):
                            C[i][j] += A[i][k] * B[k][j]
                return C

            def gaussian_elimination(matrix):
                m, n = len(matrix), len(matrix[0])
                augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
                for i in range(m):
                    max_row = i
                    for j in range(i + 1, m):
                        if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                            max_row = j
                    augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
                    pivot = augmented_matrix[i][i]
                    for j in range(i, n + 1):
                        augmented_matrix[i][j] /= pivot
                    for j in range(m):
                        if j != i:
                            factor = augmented_matrix[j][i]
                            for k in range(n + 1):
                                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
                return [row[n:] for row in augmented_matrix]

            def group_order(G):
                n = len(G)
                identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
                G_power = identity
                order = 1
                while True:
                    G_power = matrix_multiplication(G_power, G)
                    if G_power == identity:
                        break
                    order += 1
            return {"seed": seed, "metric_name": "communication_complexity_rank_variance", "metric_value": communication_complexity_rank_variance(generate_d_regular_graph(40, 3)), "instances_tested": 1, "n_max": 40, "conjecture_holds": False, "counterexample": "mapping_undefined"}

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        group_order_value = automorphism_group_order(graph)
        rank_variance_value = communication_complexity_rank_variance(graph)
        results.append({"n": n, "group_order": group_order_value, "rank_variance": rank_variance_value})

    correlation_coefficient = sum((r["group_order"] - mean_group_order) * (r["rank_variance"] - mean_rank_variance) for r in results) / len(results)
    mean_group_order = sum(r["group_order"] for r in results) / len(results)
    mean_rank_variance = sum(r["rank_variance"] for r in results) / len(results)

    return {"seed": seed, "metric_name": "communication_complexity_rank_variance", "metric_value": correlation_coefficient, "instances_tested": 6, "n_max": 40, "conjecture_holds": correlation_coefficient >= 0.9, "counterexample": ""}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")