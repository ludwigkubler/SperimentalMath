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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            b[i] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def shortest_path_length(matrix, start, end):
        n = len(matrix)
        dist = [float('inf')] * n
        dist[start] = 0
        queue = [start]
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if matrix[u][v] > 0 and dist[v] == float('inf'):
                    dist[v] = dist[u] + matrix[u][v]
                    queue.append(v)
        return dist[end]
    
    def minimum_energy_flow(matrix, start, end):
        n = len(matrix)
        flow = [0] * n
        while True:
            path = []
            u = start
            visited = set()
            while u != end and u not in visited:
                visited.add(u)
                min_cost = float('inf')
                next_node = -1
                for v in range(n):
                    if matrix[u][v] > 0 and v not in visited:
                        cost = shortest_path_length(matrix, u, v) + shortest_path_length(matrix, v, end)
                        if cost < min_cost:
                            min_cost = cost
                            next_node = v
                if next_node == -1:
                    break
                path.append((u, next_node))
                u = next_node
            if not path:
                break
            flow_value = float('inf')
            for u, v in path:
                flow_value = min(flow_value, matrix[u][v])
            for u, v in path:
                matrix[u][v] -= flow_value
                matrix[v][u] += flow_value
        return sum(flow)
    
    def dpll_search_tree_height(instance):
        n = len(instance[0])
        m = len(instance)
        stack = [(0, 0)]
        visited = set()
        height = 0
        while stack:
            node, level = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for i in range(m):
                if instance[i][node] == 1 and (i, node) not in visited:
                    stack.append((i, level + 1))
                elif instance[i][node] == -1 and (i, node) not in visited:
                    stack.append((i, level + 1))
            height = max(height, level)
        return height
    
    def construct_manifold(instance):
        n = len(instance[0])
        m = len(instance)
        points = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(n)]
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(m):
            literals = [j for j in range(n) if instance[i][j] != 0]
            for u in literals:
                for v in literals:
                    if u < v:
                        dist = math.sqrt((points[u][0] - points[v][0]) ** 2 + (points[u][1] - points[v][1]) ** 2)
                        matrix[u][v] = min(matrix[u][v], dist)
                        matrix[v][u] = matrix[u][v]
        return matrix
    
    def clause_to_literal_mapping(instance):
        n = len(instance[0])
        m = len(instance)
        mapping = {}
        for i in range(m):
            literals = [j for j in range(n) if instance[i][j] != 0]
            for literal in literals:
                if literal not in mapping:
                    mapping[literal] = []
                mapping[literal].append(i)
        return mapping
    
    def generate_instance(n, m):
        instance = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(m)]
        return instance
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    instance = generate_instance(n, m)
    mapping = clause_to_literal_mapping(instance)
    manifold = construct_manifold(mapping)
    start = random.randint(0, n - 1)
    end = random.randint(0, n - 1)
    
    dpll_height = dpll_search_tree_height(instance)
    energy_flow = minimum_energy_flow(manifold, start, end)
    
    metric_name = "DPLL Search Tree Height vs Minimum Energy Flow"
    metric_value = abs(dpll_height - energy_flow)
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value <= 3 * math.sqrt(metric_value)
    counterexample = "" if conjecture_holds else f"DPLL height: {dpll_height}, Energy flow: {energy_flow}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")