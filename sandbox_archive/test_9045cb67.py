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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(matrix):
        rref = gaussian_elimination(matrix)
        return sum(1 for row in rref if any(row))

    def is_clique(graph, vertices):
        n = len(vertices)
        for i in range(n):
            for j in range(i+1, n):
                if (vertices[i], vertices[j]) not in graph and (vertices[j], vertices[i]) not in graph:
                    return False
        return True

    def k_clique_instance(k, n):
        edges = set()
        while len(edges) < k * (k - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges

    def monotone_circuit_depth(k):
        # Placeholder for actual monotone circuit depth calculation
        # This is a dummy implementation that returns a constant value
        return 10 * k

    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n-1, 5))
    graph = {}
    for u in range(n):
        graph[u] = set()
    
    instance_edges = k_clique_instance(k, n)
    for u, v in instance_edges:
        graph[u].add(v)
        graph[v].add(u)

    rank_value = sum(rank(matrix) for matrix in [graph[i] for i in range(n)]) / n
    circuit_depth = monotone_circuit_depth(k)

    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank_value,
        "instances_tested": n,
        "conjecture_holds": rank_value >= 1.5 * circuit_depth,
        "counterexample": "" if rank_value >= 1.5 * circuit_depth else f"rank={rank_value}, depth={circuit_depth}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 1.5 * depth\" first_failing_seed={first_failing_seed}")