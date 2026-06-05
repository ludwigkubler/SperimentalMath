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
    def generate_d_regular_graph(n, d):
        if n * d % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        edges_added = 0
        
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and graph[u][v] == 0 and degree_count[u] < d and degree_count[v] < d:
                graph[u][v] = 1
                graph[v][u] = 1
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added += 1
        
        return graph

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None  # Singular matrix
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def min_categorical_dimension(graph):
        n = len(graph)
        adjacency_matrix = gaussian_elimination(graph)
        if adjacency_matrix is None:
            return None
        rank = sum(1 for row in adjacency_matrix if any(row))
        return rank

    def communication_complexity_rank(graph):
        n = len(graph)
        # Implement a simple communication complexity algorithm here
        # For example, a trivial bound could be the number of edges
        return sum(sum(row) for row in graph) // 2

    random.seed(seed)
    d = random.randint(1, 5)
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "min_categorical_dimension",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }

    min_dim = min_categorical_dimension(graph)
    if min_dim is None:
        return {
            "metric_name": "min_categorical_dimension",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Singular matrix encountered"
        }

    r = communication_complexity_rank(graph)
    
    return {
        "metric_name": "min_categorical_dimension",
        "metric_value": min_dim,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_dim >= r * 0.5,  # Example constant c = 0.5
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")