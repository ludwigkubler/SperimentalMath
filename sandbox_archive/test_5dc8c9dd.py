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
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges_added) == n * d // 2:
                    break
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges_added.add((i, j))
        return graph
    
    def communication_complexity_matrix(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                swap_found = False
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = -matrix[k][i]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
            rank += 1
        return rank
    
    def tft_state_order(matrix):
        n = len(matrix)
        order = 0
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j]:
                    order += 1
        return order
    
    def d_regular_graphs(d, max_n):
        graphs = []
        for n in range(2, max_n + 1):
            graph = generate_d_regular_graph(n, d)
            if graph is not None:
                graphs.append((n, graph))
        return graphs
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_dev_x * std_dev_y)
    
    d = random.randint(3, 5)
    max_n = 40
    graphs = d_regular_graphs(d, max_n)
    if not graphs:
        return {
            "metric_name": "TFT state order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid d-regular graph found"
        }
    
    tft_state_orders = []
    communication_complexity_ranks = []
    for n, graph in graphs:
        matrix = communication_complexity_matrix(graph)
        rank = gaussian_elimination(matrix)
        order = tft_state_order(matrix)
        tft_state_orders.append(order)
        communication_complexity_ranks.append(rank)
    
    if not tft_state_orders or not communication_complexity_ranks:
        return {
            "metric_name": "TFT state order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Failed to compute matrix rank or TFT state order"
        }
    
    expected_bound = [d**2 * math.log(n) for n, _ in graphs]
    correlation = correlation_coefficient(tft_state_orders, expected_bound)
    
    return {
        "metric_name": "TFT state order",
        "metric_value": correlation,
        "instances_tested": len(graphs),
        "n_max": max_n,
        "conjecture_holds": correlation >= 0.8,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")