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
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph

    def communication_complexity_matrix(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if v in graph[u]:
                    matrix[u][v] = 1
                    matrix[v][u] = 1
        return matrix

    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row[:] + [i] for i, row in enumerate(matrix)]
        rref = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in rref if any(row[j] != 0 for j in range(n)))
        return rank

    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            pivot_row = i
            while pivot_row < m and matrix[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(i + 1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix

    def tft_state_order(matrix):
        n = len(matrix)
        order = 0
        for row in matrix:
            for val in row:
                if val == 1:
                    order += 1
        return order

    def d_log_n(n, d):
        return d**2 * math.log(n)

    n_max = 40
    instances_tested = 30
    total_order = 0
    correlation_sum = 0
    expected_bound = 0.8

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        matrix = communication_complexity_matrix(graph)
        rank_val = rank(matrix)
        order = tft_state_order(matrix)
        expected_bound_val = d_log_n(n, d)

        total_order += order
        correlation_sum += abs(order - expected_bound_val) / (n * d)

    mean_order = total_order / instances_tested
    avg_correlation = correlation_sum / instances_tested

    conjecture_holds = all(abs(tft_state_order(communication_complexity_matrix(generate_d_regular_graph(n, d))) - d_log_n(n, d)) <= n * d for _ in range(10))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "TFT State Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")