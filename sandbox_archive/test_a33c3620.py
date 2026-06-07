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
        if n * (n - 1) // 2 < d * n:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    edges_added.add((u, v))
                    break
        return graph
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r
    
    def geometric_entanglement(C):
        n = len(C)
        det = 1.0
        for i in range(n):
            for j in range(i+1, n):
                det *= C[i][j]
        return abs(det)
    
    def communication_complexity_rank_variance(C):
        r = rank(C)
        return (n - r) / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            return {
                "metric_name": "geometric_entanglement",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "invalid_d_regular_graph"
            }
        C = graph
        E_G = geometric_entanglement(C)
        Var_C_G = communication_complexity_rank_variance(C)
        results.append((E_G, Var_C_G))
    
    if len(results) < 30:
        return {
            "metric_name": "geometric_entanglement",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    E_G_values = [res[0] for res in results]
    Var_C_G_values = [res[1] for res in results]
    
    correlation_coefficient = sum((E_G_values[i] - mean(E_G_values)) * (Var_C_G_values[i] - mean(Var_C_G_values)) for i in range(len(results))) / (len(results) * std(E_G_values) * std(Var_C_G_values))
    ratio_mean = mean([E_G / Var_C_G for E_G, Var_C_G in results])
    
    return {
        "metric_name": "geometric_entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(ratio_mean - 1) <= 2,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    avg = mean(lst)
    return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = mean([res["metric_value"] for res in results])
        std_value = std([res["metric_value"] for res in results])
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")