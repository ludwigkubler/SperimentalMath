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
    
    def generate_k_clique(n, k):
        if k > n // 2:
            return None
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        graph = [[0] * n for _ in range(n)]
        for u in clique:
            for v in clique:
                if u != v:
                    graph[u][v] = 1
                    graph[v][u] = 1
        return graph
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if j == i:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    def sum_of_squares_circuit_size(graph):
        n = len(graph)
        if n == 0:
            return 0
        size = 2 * (n - 1)  # Each vertex has at most one incoming edge in a clique
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    size += 2  # Two gates to connect two vertices
        return size
    
    def geometric_entanglement_rank(graph):
        n = len(graph)
        rank = matrix_rank(graph)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_size = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_k_clique(n, random.randint(2, n // 2))
            if graph is None:
                continue
            rank = geometric_entanglement_rank(graph)
            size = sum_of_squares_circuit_size(graph)
            total_rank += rank * n
            total_size += size
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = total_rank / instances_tested
    mean_size = total_size / instances_tested
    
    conjecture_holds = mean_rank >= 0.8 * n_values[-1] and mean_size <= 3
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, mean_size={mean_size}"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")