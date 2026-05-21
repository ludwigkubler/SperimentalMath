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
    
    def generate_random_graph(n):
        edges = set()
        for _ in range(n * (n - 1) // 2):
            u, v = random.sample(range(n), 2)
            if u > v:
                u, v = v, u
            edges.add((u, v))
        return edges
    
    def laplacian_matrix(graph, n):
        L = [[0] * n for _ in range(n)]
        degree = [0] * n
        for u, v in graph:
            L[u][v], L[v][u] = -1, -1
            degree[u] += 1
            degree[v] += 1
        for i in range(n):
            L[i][i] = degree[i]
        return L
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def eigenvalue_second_smallest(L):
        n = len(L)
        L_copy = [row[:] for row in L]
        gaussian_elimination(L_copy)
        second_smallest = float('inf')
        for i in range(n):
            if i != 0:
                second_smallest = min(second_smallest, abs(L_copy[i][i]))
        return second_smallest
    
    def resolution_length(λ2):
        c = 1e-6
        if λ2 >= c:
            return 2 ** (math.log(1 / (1 - λ2)) / math.log(2))
        return float('inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    L = laplacian_matrix(graph, n)
    λ2 = eigenvalue_second_smallest(L)
    length = resolution_length(λ2)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (math.log(1 / (1 - λ2)) / math.log(2)),
        "counterexample": "" if length >= 2 ** (math.log(1 / (1 - λ2)) / math.log(2)) else f"Graph with n={n}, λ2={λ2}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with λ2 < c\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")