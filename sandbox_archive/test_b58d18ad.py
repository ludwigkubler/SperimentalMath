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
        det_A = determinant(A)
        det_B = determinant(B)
        if det_A == 0 or det_B == 0:
            return None
        return abs(det_A / det_B)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def communication_complexity_rank(A, B):
        n = len(A)
        rank_A = 0
        rank_B = 0
        for i in range(n):
            if any(A[i][j] != 0 for j in range(n)):
                rank_A += 1
            if any(B[i][j] != 0 for j in range(n)):
                rank_B += 1
        return min(rank_A, rank_B)
    
    def log2(x):
        if x <= 0:
            return None
        return math.log2(x)
    
    n = random.randint(5, 40)
    k = random.randint(3, n-1)
    vertices, edges = generate_k_clique(n, k)
    if vertices is None or edges is None:
        return {
            "metric_name": "log_minimal_Frobenius_quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "k_clique_generation_failed"
        }
    
    A, B = matrix_representation(vertices, edges)
    frob_quotient = frobenius_quotient(A, B)
    if frob_quotient is None:
        return {
            "metric_name": "log_minimal_Frobenius_quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Frobenius_quotient_calculation_failed"
        }
    
    comm_rank = communication_complexity_rank(A, B)
    if comm_rank is None:
        return {
            "metric_name": "log_minimal_Frobenius_quotient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_rank_calculation_failed"
        }
    
    log_frob_quotient = log2(frob_quotient)
    log_comm_rank = log2(comm_rank)
    
    return {
        "metric_name": "log_minimal_Frobenius_quotient",
        "metric_value": log_frob_quotient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    count_non_none = sum(1 for r in results if r["metric_value"] is not None)
    mean_metric_value = total_metric_value / count_non_none if count_non_none > 0 else None
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / count_non_none if count_non_none > 1 else None
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")