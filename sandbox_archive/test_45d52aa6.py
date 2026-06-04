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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d - len(graph[i]))
            for neighbor in neighbors:
                if (i, neighbor) not in edges_added and (neighbor, i) not in edges_added:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges_added.add((i, neighbor))
        return graph
    
    def jones_polynomial(graph):
        n = len(graph)
        if n == 0:
            return 1
        if n == 1:
            return 1
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        for u, v in graph:
            M[u][v] = -1
            M[v][u] = -1
        det = determinant(M)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def circuit_depth(graph):
        n = len(graph)
        if n == 0:
            return 0
        depth = [0] * n
        queue = []
        for i in range(n):
            if len(graph[i]) == 1:
                queue.append(i)
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                depth[neighbor] = max(depth[neighbor], depth[node] + 1)
                graph[neighbor].remove(node)
                if len(graph[neighbor]) == 1 and depth[neighbor] > 0:
                    queue.append(neighbor)
        return max(depth)
    
    def local_indeterminacy(jones_poly):
        # Simplified version for demonstration
        return abs(jones_poly)
    
    n_values = [5, 10, 15, 20, 30, 40]
    indet_sum = 0
    depth_sum = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        jones_poly = jones_polynomial(graph)
        indet = local_indeterminacy(jones_poly)
        depth = circuit_depth(graph)
        indet_sum += indet
        depth_sum += depth
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "local_indeterminacy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_indet = indet_sum / instances_tested
    mean_depth = depth_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(indet * depth for indet, depth in zip(indet_values, depth_values)) - indet_sum * depth_sum) / \
                               math.sqrt((instances_tested * sum(indet ** 2 for indet in indet_values) - indet_sum ** 2) *
                                          (instances_tested * sum(depth ** 2 for depth in depth_values) - depth_sum ** 2))
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_depth - mean_indet) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")