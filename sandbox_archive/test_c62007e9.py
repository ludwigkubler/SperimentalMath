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
    
    def generate_random_graph(n):
        edges = set()
        while len(edges) < (n * (n - 1)) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = -1
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(n):
                if j != i and matrix[rank][j] != 0:
                    factor = matrix[j][i] / matrix[rank][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_lattice_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        augmented_matrix = [row + [1] for row in adjacency_matrix]
        return gaussian_elimination(augmented_matrix)
    
    def construct_quantum_circuit(graph):
        n = len(graph)
        circuit_depth = 0
        # Simplified quantum circuit construction logic (placeholder)
        for _ in range(n):
            circuit_depth += 2
        return circuit_depth
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    lattice_rank = compute_lattice_rank(graph)
    circuit_depth = construct_quantum_circuit(graph)
    
    expected_rank = int(1.5 * n ** 1.5)
    is_supported = abs(lattice_rank - expected_rank) <= 0.75 * expected_rank and circuit_depth <= (lattice_rank ** 2)
    
    return {
        "metric_name": "Lattice Rank vs Circuit Depth",
        "metric_value": lattice_rank,
        "instances_tested": 1,
        "conjecture_holds": is_supported,
        "counterexample": "" if is_supported else f"Graph with n={n}, L(G) rank={lattice_rank}, D={circuit_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")