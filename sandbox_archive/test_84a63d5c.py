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
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        return vertices, edges
    
    def matrix_representation(vertices, edges):
        n = len(vertices)
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
            B[u][v] = 1
            B[v][u] = 1
        return A, B
    
    def frobenius_quotient(A, B):
        n = len(A)
        numerator = sum(sum((A[i][j] - B[i][j]) ** 2 for j in range(n)) for i in range(n))
        denominator = sum(sum(A[i][j] ** 2 for j in range(n)) for i in range(n))
        if denominator == 0:
            return None
        return numerator / denominator
    
    def communication_complexity_rank(A, B):
        n = len(A)
        rank_A = gaussian_elimination(A)
        rank_B = gaussian_elimination(B)
        return min(rank_A, rank_B)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    def log2(x):
        if x <= 0:
            return None
        return math.log2(x)
    
    n = random.randint(5, 40)
    k = min(n, random.randint(3, n // 2))
    vertices, edges = generate_k_clique(n, k)
    if vertices is None or edges is None:
        return {
            "metric_name": "Frobenius Quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "k_clique_generation_failed"
        }
    
    A, B = matrix_representation(vertices, edges)
    frob_quotient = frobenius_quotient(A, B)
    comm_complexity_rank = communication_complexity_rank(A, B)
    
    if frob_quotient is None or comm_complexity_rank is None:
        return {
            "metric_name": "Frobenius Quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "matrix_representation_failed"
        }
    
    if frob_quotient == 0:
        return {
            "metric_name": "Frobenius Quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "frob_quotient_zero"
        }
    
    log_frob_quotient = log2(frob_quotient)
    if log_frob_quotient is None:
        return {
            "metric_name": "Frobenius Quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "log2_frob_quotient_failed"
        }
    
    return {
        "metric_name": "Frobenius Quotient",
        "metric_value": log_frob_quotient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")