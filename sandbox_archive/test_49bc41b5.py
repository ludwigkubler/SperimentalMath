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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_d_regular_graph(d, n):
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def matrix_representation(graph):
        n = len(graph)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                M[i][j] = 1
                M[j][i] = 1
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(M[k][i]) > abs(M[max_row][i]):
                    max_row = k
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        rank = sum(1 for row in M if any(row))
        return rank
    
    def boolean_circuit_entanglement_complexity(graph):
        n = len(graph)
        # Simplified heuristic: number of edges
        return sum(len(neighbors) for neighbors in graph.values()) // 2
    
    d = random.randint(3, 5)
    n = random.randint(5, 10)
    G = generate_d_regular_graph(d, n)
    M = matrix_representation(G)
    rank = gaussian_elimination(M)
    if rank is None:
        return {
            "metric_name": "Algebraic K-theory Rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    entanglement_complexity = boolean_circuit_entanglement_complexity(G)
    
    return {
        "metric_name": "Algebraic K-theory Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
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
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not enough supporting data\" first_failing_seed={first_failing_seed}")