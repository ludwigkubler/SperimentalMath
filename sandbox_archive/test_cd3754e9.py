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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def pinv(A):
        m, n = len(A), len(A[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        augmented_matrix = [A[i] + I[i] for i in range(m)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        pinv_A = [[reduced_matrix[i][j+n] / reduced_matrix[i][i] if i == j else 0 for j in range(n)] for i in range(m)]
        return pinv_A

    def max_cut(G):
        n = len(G)
        cuts = [1 << i for i in range(1, 1 << (n - 1))]
        best_cut_value = 0
        for cut in cuts:
            cut_value = sum(G[i][j] if ((cut >> i) & 1) and ((cut >> j) & 1) else 0 for i in range(n) for j in range(i + 1, n))
            best_cut_value = max(best_cut_value, cut_value)
        return best_cut_value

    def adjacency_matrix(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        return A

    def laplacian_matrix(A):
        n = len(A)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(A[i])
            L[i][i] = degree
            for j in range(i + 1, n):
                L[i][j] = -A[i][j]
                L[j][i] = -A[i][j]
        return L

    def hessian_matrix(G, A, L_inv):
        n = len(G)
        m = len(G[0])
        H = [[0] * m for _ in range(m)]
        for e1 in range(m):
            u1, v1 = G[e1]
            p_e1 = L_inv[u1][u1] + L_inv[v1][v1] - 2 * L_inv[u1][v1]
            for e2 in range(e1 + 1, m):
                u2, v2 = G[e2]
                y_e1e2 = L_inv[u1][u2] - L_inv[u1][v2] - L_inv[v1][u2] + L_inv[v1][v2]
                H[e1][e2] = p_e1 * p_e2 - y_e1e2 ** 2
        return H

    def eigenvalues(H):
        n = len(H)
        A = [[H[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            A[i][i] -= max(abs(A[i][j]) for j in range(i + 1, n))
        eigs = [A[i][i] for i in range(n)]
        return sorted(eigs)

    def delorme_poljak_bound(G, A, λ_min):
        n = len(G)
        m = len(G[0])
        return m / 2 + (n / 4) * abs(λ_min)

    def lorentzian_hessian_gap(H):
        eigs = eigenvalues(H)
        return eigs[-1] - eigs[-2]

    n = random.randint(6, 30)
    p = random.choice([0.4, 0.5, 0.6])
    G = []
    while len(G) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if (u, v) not in G and (v, u) not in G:
            G.append((u, v))
    A = adjacency_matrix(G)
    L_inv = pinv(laplacian_matrix(A))
    H = hessian_matrix(G, A, L_inv)
    λ_min = min(eigenvalues(A))
    g_G = lorentzian_hessian_gap(H)
    MaxCut_G = max_cut(G)
    DP_G = delorme_poljak_bound(G, A, λ_min)
    ratio = (DP_G - MaxCut_G) / (g_G * n)

    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1e-3 and all(ratio >= 1e-3 for _ in range(5)),
        "counterexample": "" if ratio >= 1e-3 else f"Ratio {ratio} < 1e-3"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {result['metric_value']} < 1e-3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")