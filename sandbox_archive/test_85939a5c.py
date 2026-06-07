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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def commute(A, B):
        return matrix_multiply(matrix_multiply(A, B), matrix_multiply(B, A)) == matrix_multiply(matrix_multiply(B, A), matrix_multiply(A, B))
    
    def commuting_matrix(G):
        n = len(G)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        C = [I]
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v]:
                    H = [[0] * n for _ in range(n)]
                    H[u][u], H[v][v], H[u][v], H[v][u] = 1, -1, -1, 1
                    C.append(H)
        return C
    
    def geometric_entanglement(C):
        m = len(C)
        A = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                if commute(C[i], C[j]):
                    A[i][j], A[j][i] = 1, 1
        return sum(sum(row) for row in A)
    
    def communication_complexity_rank_variance(C):
        m, n = len(C), len(C[0])
        rank = 0
        for i in range(m):
            if any(C[i][j] != 0 for j in range(n)):
                rank += 1
        return (rank - 1) ** 2
    
    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        edges_added = 0
        while edges_added < d * n // 2:
            u = random.randint(0, n-1)
            v = random.choice([i for i in range(n) if i != u and G[u][i] == 0])
            G[u][v], G[v][u] = 1, 1
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added += 1
        return G
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * (n - 1) // 2 < d * n:
            continue
        G = generate_d_regular_graph(n, d)
        C = commuting_matrix(G)
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
    
    E_G_sum = sum(E for E, _ in results)
    Var_C_G_sum = sum(V for _, V in results)
    corr_coeff = (sum((E - E_G_sum / len(results)) * (V - Var_C_G_sum / len(results)) for E, V in results) /
                  math.sqrt(sum((E - E_G_sum / len(results)) ** 2 for E, _ in results) *
                            sum((V - Var_C_G_sum / len(results)) ** 2 for _, V in results)))
    ratio_mean = E_G_sum / Var_C_G_sum
    
    return {
        "metric_name": "geometric_entanglement",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr_coeff) >= 0.8 and abs(ratio_mean - 1) <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    corr_coeffs = [r["metric_value"] for r in results if r["metric_value"] is not None]
    ratio_means = [r["metric_value"] for r in results if r["metric_value"] is not None and r["conjecture_holds"]]
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(corr_coeffs)/len(corr_coeffs):.2f} std={math.sqrt(sum((c - sum(corr_coeffs)/len(corr_coeffs))**2 for c in corr_coeffs)/len(corr_coeffs)):.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(corr_coeffs)/len(corr_coeffs):.2f} std={math.sqrt(sum((c - sum(corr_coeffs)/len(corr_coeffs))**2 for c in corr_coeffs)/len(corr_coeffs)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")