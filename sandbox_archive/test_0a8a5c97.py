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
    
    def is_3_regular(G):
        degree = [0] * len(G)
        for u, v in G:
            degree[u] += 1
            degree[v] += 1
        return all(d == 3 for d in degree)

    def generate_random_3_regular(n):
        while True:
            edges = set()
            nodes = list(range(n))
            random.shuffle(nodes)
            for i in range(n):
                for j in range(i + 1, n):
                    if (nodes[i], nodes[j]) not in edges and (nodes[j], nodes[i]) not in edges:
                        edges.add((nodes[i], nodes[j]))
                        break
                else:
                    continue
                break
            G = [set() for _ in range(n)]
            for u, v in edges:
                G[u].add(v)
                G[v].add(u)
            if is_3_regular(G):
                return G

    def compute_eigenvalues(M):
        n = len(M)
        eigenvalues = []
        V = [[1] * n]
        for _ in range(80):
            V_next = [sum(V[j][k] * M[k][i] for k in range(n)) / math.sqrt(sum(x * x for x in V[j])) for j in range(n)]
            V_next = [v / math.sqrt(sum(x * x for x in v)) for v in V_next]
            eigenvalues.append(max(abs(eig) for eig in compute_eigenvalues(V_next)))
        return eigenvalues

    def QR_iterations(A):
        n = len(A)
        Q, R = [[0] * n for _ in range(n)], [[0] * n for _ in range(n)]
        for i in range(n):
            Q[i][i] = 1
        for k in range(n - 1):
            v = [A[i][k] for i in range(k, n)]
            norm = math.sqrt(sum(x * x for x in v))
            v[k] += norm
            u = [x / norm for x in v]
            Q_k = [[0] * n for _ in range(n)]
            R_k = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i <= k:
                        Q_k[i][j] = Q[i][j]
                    if j >= k:
                        R_k[i][j] = A[i][j]
                    if i == j and i > k:
                        R_k[i][i] -= sum(u[j] * v[j] for j in range(k + 1, n))
            Q = matrix_multiply(Q_k, Q)
            R = matrix_multiply(R_k, R)
        return Q, R

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
        return C

    def compute_M_G(G, n):
        r = math.ceil(math.sqrt(2 * n))
        V = [[1] * n]
        lambda_max = max(abs(eig) for eig in compute_eigenvalues(V))
        step_size = 0.1 / lambda_max
        for _ in range(80):
            V_next = [sum(V[j][k] * G[k][i] for k in range(n)) for j in range(n)]
            V_next = [v / math.sqrt(sum(x * x for x in v)) for v in V_next]
            V = V_next
        M_G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M_G[i][j] = sum(V[j][k] * V[k][i] for k in range(n))
        return M_G

    def compute_R(G, n):
        eigenvalues = compute_eigenvalues(M_G)
        count = sum(1 for eig in eigenvalues if -1 + 1 / math.sqrt(n) < eig < 1 - 1 / math.sqrt(n))
        return count / n

    def compute_max_cut(G):
        n = len(G)
        max_cut_value = -1
        for mask in range(1 << n):
            cut_value = sum(G[i][j] if (mask & (1 << i)) and not (mask & (1 << j)) else 0 for i in range(n) for j in range(i + 1, n))
            max_cut_value = max(max_cut_value, cut_value)
        return max_cut_value

    def compute_spectral_upper_bound(G):
        n = len(G)
        lambda_max = max(abs(eig) for eig in compute_eigenvalues(G))
        return n * lambda_max / 4 + sum(len(G[i]) for i in range(n)) / 2

    n_values = [8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        G = generate_random_3_regular(n)
        M_G = compute_M_G(G, n)
        R_G = compute_R(G, n)
        max_cut_value = compute_max_cut(G) if n <= 20 else compute_spectral_upper_bound(G)
        SDP_ratio = R_G / (max_cut_value / 4)
        
        results.append({
            "metric_name": "R(G)/n",
            "metric_value": R_G,
            "instances_tested": 1,
            "conjecture_holds": SDP_ratio >= 0.878 and R_G / n >= 0.55,
            "counterexample": ""
        })
    
    mean_R = sum(result["metric_value"] for result in results) / len(results)
    std_R = math.sqrt(sum((result["metric_value"] - mean_R) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - mean_R) <= 0.07) / len(results)

    return {
        "seed": seed,
        "mean_R": mean_R,
        "std_R": std_R,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_R = sum(r["mean_R"] for r in results) / len(results)
    std_R = math.sqrt(sum((r["mean_R"] - mean_R) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["mean_R"] - mean_R) <= 0.07) / len(results)
    
    if all(result["support_fraction"] >= 0.85 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SDP_ratio < 0.878 or R_G/n < 0.55\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")