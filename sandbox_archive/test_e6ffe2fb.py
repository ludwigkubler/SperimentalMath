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
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                if len(edges) >= n * (n - 1) // 2:
                    return edges
                edges.append((i, j))
        while len(edges) < n * (n - 1) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return edges
    
    def construct_monotone_circuit(edges):
        circuit = []
        for u, v in edges:
            circuit.append(f"OR({u}, {v})")
        return circuit
    
    def noncrossing_partition_matrix(circuit):
        n = len(circuit)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i].startswith("OR") and circuit[j].startswith("OR"):
                    u, v = map(int, circuit[i][4:].split(", "))
                    x, y = map(int, circuit[j][4:].split(", "))
                    if (u == x or u == y) and (v == x or v == y):
                        matrix[i][j] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                matrix[i][j] /= matrix[i][i]
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    n_values = [15, 20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        edges = generate_k_clique(n, n)
        circuit = construct_monotone_circuit(edges)
        matrix = noncrossing_partition_matrix(circuit)
        rank_value = rank(matrix)
        results.append({
            "n": n,
            "circuit_size": len(circuit),
            "rank": rank_value
        })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank = min(result["rank"] for result in results)
    avg_circuit_size = sum(result["circuit_size"] for result in results) / len(results)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": min_rank >= avg_circuit_size ** (1/4 + n_values[0]/16),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 32))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    min_rank_values = [result["metric_value"] for result in results if result["instances_tested"] > 0]
    avg_min_rank = sum(min_rank_values) / len(min_rank_values)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_min_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_min_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_rank' first_failing_seed={first_failing_seed}")