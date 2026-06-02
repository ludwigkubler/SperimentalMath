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
    
    def generate_graph(n):
        edges = set()
        for _ in range(2 * n - 1):
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def laplacian_matrix(edges, n):
        L = [[0] * n for _ in range(n)]
        degree = [0] * n
        for u, v in edges:
            L[u][v] = -1
            L[v][u] = -1
            degree[u] += 1
            degree[v] += 1
        for i in range(n):
            L[i][i] = degree[i]
        return L
    
    def normalize_matrix(M, n):
        D_inv = [[0] * n for _ in range(n)]
        for i in range(n):
            if M[i][i] == 0:
                continue
            D_inv[i][i] = Fraction(1, M[i][i])
        return [[D_inv[i][j] * M[i][j] for j in range(n)] for i in range(n)]
    
    def smallest_non_zero_eigenvalue(L):
        n = len(L)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A = L
        B = I
        tol = Fraction(1, 10**6)
        max_iter = 1000
        for _ in range(max_iter):
            Q, R = qr_decomposition(A)
            A = R @ Q
            if abs(A[0][0]) < tol:
                break
        return A[0][0]
    
    def qr_decomposition(M):
        n = len(M)
        Q = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        R = [[M[i][j] if i <= j else Fraction(0) for j in range(n)] for i in range(n)]
        for k in range(n):
            v = [R[i][k] for i in range(k, n)]
            norm = sum(vi * vi for vi in v).sqrt()
            Q[k][k] = Fraction(v[k], norm)
            for j in range(k + 1, n):
                R[j][k] = sum(Q[i][k] * M[i][j] for i in range(k, n))
                Q[j][k] = sum(Q[i][k] * v[i] for i in range(k, n)) / norm
        return Q, R
    
    def communication_complexity_rank(edges):
        degrees = [0] * len(edges)
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        return min(degrees)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            edges = generate_graph(n)
            L = laplacian_matrix(edges, n)
            L_norm = normalize_matrix(L, n)
            lambda_min = smallest_non_zero_eigenvalue(L_norm)
            r_f = communication_complexity_rank(edges)
            results.append({
                "n": n,
                "lambda_min": lambda_min,
                "r_f": r_f
            })
    
    if not results:
        return {
            "metric_name": "log(r(f)) / log(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lambda_min_avg = sum(res["lambda_min"] for res in results) / len(results)
    r_f_avg = sum(res["r_f"] for res in results) / len(results)
    log_r_f_avg = math.log(r_f_avg)
    log_n_avg = math.log(n_values[-1])
    
    if lambda_min_avg <= 0.5 * log_n_avg:
        return {
            "metric_name": "log(r(f)) / log(n)",
            "metric_value": log_r_f_avg,
            "instances_tested": len(results),
            "n_max": n_values[-1],
            "conjecture_holds": False,
            "counterexample": f"lambda_min_avg={lambda_min_avg} <= 0.5 * log_n_avg={0.5 * log_n_avg}"
        }
    else:
        return {
            "metric_name": "log(r(f)) / log(n)",
            "metric_value": log_r_f_avg,
            "instances_tested": len(results),
            "n_max": n_values[-1],
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")