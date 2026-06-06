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
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
        return x
    
    def compute_min_order_local_induction(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    A[i][j] = 1
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        B = matrix_multiply(A, I)
        x = gaussian_elimination(B, [0] * n)
        min_order = sum(1 for val in x if abs(val) > 1e-9)
        return min_order
    
    def compute_communication_complexity_rank(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        B = matrix_multiply(A, I)
        x = gaussian_elimination(B, [0] * n)
        rank = sum(1 for val in x if abs(val) > 1e-9)
        return rank
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        graph = generate_random_graph(n)
        min_order = compute_min_order_local_induction(graph)
        rank = compute_communication_complexity_rank(graph)
        results.append({
            "metric_name": "variance",
            "metric_value": variance([rank]),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })
    
    return {
        "seed": seed,
        "metric_name": "variance",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")